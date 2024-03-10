from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Iterable, TypeAlias

from sentencepiece import SentencePieceProcessor

import pygptprompt.gguf as gguf
from pygptprompt.gguf.gguf_writer import GGUFWriter

#
# vocab
#

Vocab: TypeAlias = "BpeVocab | SentencePieceVocab | HfVocab"


class BpeVocab:
    def __init__(self, fname_tokenizer: Path, fname_added_tokens: Path | None) -> None:
        self.bpe_tokenizer = json.loads(
            open(str(fname_tokenizer), encoding="utf-8").read()
        )
        if isinstance(self.bpe_tokenizer.get("model"), dict):
            self.vocab = self.bpe_tokenizer["model"]["vocab"]
        else:
            self.vocab = self.bpe_tokenizer
        added_tokens: dict[str, int]
        if fname_added_tokens is not None:
            # FIXME: Verify that added tokens here _cannot_ overlap with the main vocab.
            added_tokens = json.load(open(fname_added_tokens, encoding="utf-8"))
        else:
            # Fall back to trying to find the added tokens in tokenizer.json
            tokenizer_json_file = fname_tokenizer.parent / "tokenizer.json"
            if not tokenizer_json_file.is_file():
                added_tokens = {}
            else:
                tokenizer_json = json.load(open(tokenizer_json_file, encoding="utf-8"))
                added_tokens = dict(
                    (item["content"], item["id"])
                    for item in tokenizer_json.get("added_tokens", [])
                    # Added tokens here can be duplicates of the main vocabulary.
                    if item["content"] not in self.bpe_tokenizer
                )

        vocab_size: int = len(self.vocab)
        expected_ids = list(range(vocab_size, vocab_size + len(added_tokens)))
        actual_ids = sorted(added_tokens.values())
        if expected_ids != actual_ids:
            expected_end_id = vocab_size + len(actual_ids) - 1
            raise Exception(
                f"Expected the {len(actual_ids)} added token ID(s) to be sequential in the range {vocab_size} - {expected_end_id}; got {actual_ids}"
            )

        items = sorted(added_tokens.items(), key=lambda text_idx: text_idx[1])
        self.added_tokens_dict = added_tokens
        self.added_tokens_list = [text for (text, idx) in items]
        self.vocab_size_base: int = vocab_size
        self.vocab_size: int = self.vocab_size_base + len(self.added_tokens_list)
        self.fname_tokenizer = fname_tokenizer
        self.fname_added_tokens = fname_added_tokens

    def bpe_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        reverse_vocab = {id: encoded_tok for encoded_tok, id in self.vocab.items()}

        for i, _ in enumerate(self.vocab):
            yield reverse_vocab[i], 0.0, gguf.TokenType.NORMAL

    def added_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        for text in self.added_tokens_list:
            score = -1000.0
            yield text.encode("utf-8"), score, gguf.TokenType.CONTROL

    def all_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        yield from self.bpe_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<BpeVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"


class SentencePieceVocab:
    def __init__(self, fname_tokenizer: Path, fname_added_tokens: Path | None) -> None:
        self.sentencepiece_tokenizer = SentencePieceProcessor(str(fname_tokenizer))
        added_tokens: dict[str, int]
        if fname_added_tokens is not None:
            added_tokens = json.load(open(fname_added_tokens, encoding="utf-8"))
        else:
            added_tokens = {}

        vocab_size: int = self.sentencepiece_tokenizer.vocab_size()

        new_tokens = {
            id: piece for piece, id in added_tokens.items() if id >= vocab_size
        }
        expected_new_ids = list(range(vocab_size, vocab_size + len(new_tokens)))
        actual_new_ids = sorted(new_tokens.keys())

        if expected_new_ids != actual_new_ids:
            raise ValueError(
                f"Expected new token IDs {expected_new_ids} to be sequential; got {actual_new_ids}"
            )

        # Token pieces that were added to the base vocabulary.
        self.added_tokens_dict = added_tokens
        self.added_tokens_list = [new_tokens[id] for id in actual_new_ids]
        self.vocab_size_base = vocab_size
        self.vocab_size = self.vocab_size_base + len(self.added_tokens_list)
        self.fname_tokenizer = fname_tokenizer
        self.fname_added_tokens = fname_added_tokens

    def sentencepiece_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        tokenizer = self.sentencepiece_tokenizer
        for i in range(tokenizer.vocab_size()):
            piece = tokenizer.id_to_piece(i)
            text: bytes = piece.encode("utf-8")
            score: float = tokenizer.get_score(i)

            toktype = gguf.TokenType.NORMAL
            if tokenizer.is_unknown(i):
                toktype = gguf.TokenType.UNKNOWN
            if tokenizer.is_control(i):
                toktype = gguf.TokenType.CONTROL

            # NOTE: I think added_tokens are user defined.
            # ref: https://github.com/google/sentencepiece/blob/master/src/sentencepiece_model.proto
            # if tokenizer.is_user_defined(i): toktype = gguf.TokenType.USER_DEFINED

            if tokenizer.is_unused(i):
                toktype = gguf.TokenType.UNUSED
            if tokenizer.is_byte(i):
                toktype = gguf.TokenType.BYTE

            yield text, score, toktype

    def added_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        for text in self.added_tokens_list:
            score = -1000.0
            yield text.encode("utf-8"), score, gguf.TokenType.USER_DEFINED

    def all_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        yield from self.sentencepiece_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<SentencePieceVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"


class HfVocab:
    def __init__(
        self, fname_tokenizer: Path, fname_added_tokens: Path | None = None
    ) -> None:
        try:
            from transformers import AutoTokenizer
        except ImportError as e:
            raise ImportError(
                "To use HfVocab, please install the `transformers` package. "
                "You can install it with `pip install transformers`."
            ) from e

        print("fname_tokenizer:", fname_tokenizer)
        # Allow the tokenizer to default to slow or fast versions.
        # Explicitly set tokenizer to use local paths.
        self.tokenizer = AutoTokenizer.from_pretrained(
            fname_tokenizer,
            cache_dir=fname_tokenizer,
            local_files_only=True,
        )

        # Initialize lists and dictionaries for added tokens
        self.added_tokens_list = []
        self.added_tokens_dict = dict()
        self.added_tokens_ids = set()

        # Process added tokens
        for tok, tokidx in sorted(
            self.tokenizer.get_added_vocab().items(), key=lambda x: x[1]
        ):
            # Only consider added tokens that are not in the base vocabulary
            if tokidx >= self.tokenizer.vocab_size:
                self.added_tokens_list.append(tok)
                self.added_tokens_dict[tok] = tokidx
                self.added_tokens_ids.add(tokidx)

        # Store special tokens and their IDs
        self.specials = {
            tok: self.tokenizer.get_vocab()[tok]
            for tok in self.tokenizer.all_special_tokens
        }
        self.special_ids = set(self.tokenizer.all_special_ids)

        # Set vocabulary sizes
        self.vocab_size_base = self.tokenizer.vocab_size
        self.vocab_size = self.vocab_size_base + len(self.added_tokens_list)

        self.fname_tokenizer = fname_tokenizer
        self.fname_added_tokens = fname_added_tokens

    def hf_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        reverse_vocab = {
            id: encoded_tok for encoded_tok, id in self.tokenizer.get_vocab().items()
        }

        for token_id in range(self.vocab_size_base):
            # Skip processing added tokens here
            if token_id in self.added_tokens_ids:
                continue

            # Convert token text to bytes
            token_text = reverse_vocab[token_id].encode("utf-8")

            # Yield token text, score, and type
            yield token_text, self.get_token_score(token_id), self.get_token_type(
                token_id,
                token_text,
                self.special_ids,  # Reuse already stored special IDs
            )

    def get_token_type(
        self, token_id: int, token_text: bytes, special_ids: set[int]
    ) -> gguf.TokenType:
        # Special case for byte tokens
        if re.fullmatch(rb"<0x[0-9A-Fa-f]{2}>", token_text):
            return gguf.TokenType.BYTE

        # Determine token type based on whether it's a special token
        return (
            gguf.TokenType.CONTROL if token_id in special_ids else gguf.TokenType.NORMAL
        )

    def get_token_score(self, token_id: int) -> float:
        # Placeholder for actual logic to determine the token's score
        # This needs to be implemented based on specific requirements
        return -1000.0  # Default score

    def added_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        for text in self.added_tokens_list:
            if text in self.specials:
                toktype = self.get_token_type(
                    self.specials[text], b"", self.special_ids
                )
                score = self.get_token_score(self.specials[text])
            else:
                toktype = gguf.TokenType.USER_DEFINED
                score = -1000.0

            yield text.encode("utf-8"), score, toktype

    def has_newline_token(self):
        return "<0x0A>" in self.tokenizer.vocab or "\n" in self.tokenizer.vocab

    def all_tokens(self) -> Iterable[tuple[bytes, float, gguf.TokenType]]:
        yield from self.hf_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<HfVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"


class SpecialVocab:
    merges: list[str]
    add_special_token: dict[str, bool]
    special_token_ids: dict[str, int]
    chat_template: str | None

    def __init__(
        self,
        path: str | os.PathLike[str],
        load_merges: bool = False,
        special_token_types: tuple[str, ...] | None = None,
        n_vocab: int | None = None,
    ):
        self.special_token_ids = {}
        self.add_special_token = {}
        self.n_vocab = n_vocab
        self.load_merges = load_merges
        self.merges = []
        self.chat_template = None
        if special_token_types is not None:
            self.special_token_types = special_token_types
        else:
            self.special_token_types = (
                "bos",
                "eos",
                "unk",
                "sep",
                "pad",
                "cls",
                "mask",
            )
        self._load(Path(path))

    def __repr__(self) -> str:
        return "<SpecialVocab with {} merges, special tokens {}, add special tokens {}>".format(
            len(self.merges),
            self.special_token_ids or "unset",
            self.add_special_token or "unset",
        )

    def add_to_gguf(self, gw: GGUFWriter, quiet: bool = False) -> None:
        if self.merges:
            if not quiet:
                print(f"gguf: Adding {len(self.merges)} merge(s).")
            gw.add_token_merges(self.merges)
        elif self.load_merges:
            print(
                "gguf: WARNING: Adding merges requested but no merges found, output may be non-functional.",
                file=sys.stderr,
            )
        for typ, tokid in self.special_token_ids.items():
            id_handler: Callable[[int], None] | None = getattr(
                gw, f"add_{typ}_token_id", None
            )
            if id_handler is None:
                print(
                    f"gguf: WARNING: No handler for special token type {typ} with id {tokid} - skipping",
                    file=sys.stderr,
                )
                continue
            if not quiet:
                print(f"gguf: Setting special token type {typ} to {tokid}")
            id_handler(tokid)
        for typ, value in self.add_special_token.items():
            add_handler: Callable[[bool], None] | None = getattr(
                gw, f"add_add_{typ}_token", None
            )
            if add_handler is None:
                print(
                    f"gguf: WARNING: No handler for add_{typ}_token with value {value} - skipping",
                    file=sys.stderr,
                )
                continue
            if not quiet:
                print(f"gguf: Setting add_{typ}_token to {value}")
            add_handler(value)
        if self.chat_template is not None:
            if not quiet:
                print(f"gguf: Setting chat_template to {self.chat_template}")
            gw.add_chat_template(self.chat_template)

    def _load(self, path: Path) -> None:
        self._try_load_from_tokenizer_json(path)
        self._try_load_from_config_json(path)
        if self.load_merges and not self.merges:
            self._try_load_merges_txt(path)

    def _try_load_merges_txt(self, path: Path) -> bool:
        merges_file = path / "merges.txt"
        if not merges_file.is_file():
            return False
        with open(merges_file, "r", encoding="utf-8") as fp:
            first_line = next(fp, "").strip()
            if not first_line.startswith("#"):
                fp.seek(0)
                line_num = 0
            else:
                line_num = 1
            merges = []
            for line in fp:
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                parts = line.split(None, 3)
                if len(parts) != 2:
                    print(
                        f"gguf: WARNING: {merges_file.name}: Line {line_num}: Entry malformed, ignoring",
                        file=sys.stderr,
                    )
                    continue
                merges.append(f"{parts[0]} {parts[1]}")
        self.merges = merges
        return True

    def _set_special_token(self, typ: str, tid: Any) -> None:
        if not isinstance(tid, int):
            return
        if tid < 0:
            raise ValueError(f"invalid value for special token type {typ}: {tid}")
        if self.n_vocab is None or tid < self.n_vocab:
            if typ in self.special_token_ids:
                return
            self.special_token_ids[typ] = tid
            return
        print(
            f"gguf: WARNING: Special token type {typ}, id {tid} out of range, must be under {self.n_vocab} - skipping",
            file=sys.stderr,
        )

    def _try_load_from_tokenizer_json(self, path: Path) -> bool:
        tokenizer_file = path / "tokenizer.json"
        if tokenizer_file.is_file():
            with open(tokenizer_file, encoding="utf-8") as f:
                tokenizer = json.load(f)
            if self.load_merges:
                merges = tokenizer.get("model", {}).get("merges")
                if isinstance(merges, list) and merges and isinstance(merges[0], str):
                    self.merges = merges
            added_tokens = tokenizer.get("added_tokens", {})
        else:
            added_tokens = {}
        tokenizer_config_file = path / "tokenizer_config.json"
        if not tokenizer_config_file.is_file():
            return True
        with open(tokenizer_config_file, encoding="utf-8") as f:
            tokenizer_config = json.load(f)
        chat_template = tokenizer_config.get("chat_template")
        if chat_template is None or isinstance(chat_template, str):
            self.chat_template = chat_template
        else:
            print(
                f"gguf: WARNING: Bad type for chat_template field in {tokenizer_config_file!r} - ignoring",
                file=sys.stderr,
            )
        for typ in self.special_token_types:
            add_entry = tokenizer_config.get(f"add_{typ}_token")
            if isinstance(add_entry, bool):
                self.add_special_token[typ] = add_entry
            entry = tokenizer_config.get(f"{typ}_token")
            if isinstance(entry, str):
                tc_content = entry
            elif isinstance(entry, dict):
                entry_content = entry.get("content")
                if not isinstance(entry_content, str):
                    continue
                tc_content = entry_content
            else:
                continue
            # We only need the first match here.
            maybe_token_id = next(
                (
                    atok.get("id")
                    for atok in added_tokens
                    if atok.get("content") == tc_content
                ),
                None,
            )
            self._set_special_token(typ, maybe_token_id)
        return True

    def _try_load_from_config_json(self, path: Path) -> bool:
        config_file = path / "config.json"
        if not config_file.is_file():
            return False
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
        for typ in self.special_token_types:
            self._set_special_token(typ, config.get(f"{typ}_token_id"))
        return True


class VocabFactory:
    _FILES = {"spm": "tokenizer.model", "bpe": "vocab.json", "hfft": "tokenizer.json"}

    def __init__(self, path: Path):
        self.path = path
        self.file_paths = self._detect_files()
        print(f"Found vocab files: {self.file_paths}")

    def _detect_files(self) -> dict[str, Path | None]:
        def locate(file: str) -> Path | None:
            if (path := self.path / file).exists():
                return path
            if (path := self.path.parent / file).exists():
                return path
            return None

        return {vt: locate(f) for vt, f in self._FILES.items()}

    def _select_file(self, vocab_types: list[str]) -> tuple[str, Path]:
        for vtype in vocab_types:
            try:
                path = self.file_paths[vtype]
            except KeyError:
                raise ValueError(f"Unsupported vocabulary type {vtype}") from None
            if path is not None:
                return vtype, path
        raise FileNotFoundError(
            f"Could not find any of {[self._FILES[vt] for vt in vocab_types]}"
        )

    def _create_special_vocab(
        self, vocab: Vocab, vocabtype: str, model_parent_path: Path
    ) -> gguf.SpecialVocab:
        load_merges = vocabtype == "bpe"
        n_vocab = vocab.vocab_size if hasattr(vocab, "vocab_size") else None
        return gguf.SpecialVocab(
            model_parent_path,
            load_merges=load_merges,
            special_token_types=None,  # Predetermined or passed as a parameter
            n_vocab=n_vocab,
        )

    def load_vocab(
        self, vocab_types: list[str], model_parent_path: Path
    ) -> tuple[Vocab, gguf.SpecialVocab]:
        vocab_type, path = self._select_file(vocab_types)
        print(f"Loading vocab file {path!r}, type {vocab_type!r}")

        added_tokens_path = path.parent / "added_tokens.json"
        vocab: Vocab
        if vocab_type == "bpe":
            vocab = BpeVocab(
                path, added_tokens_path if added_tokens_path.exists() else None
            )
        elif vocab_type == "spm":
            vocab = SentencePieceVocab(
                path, added_tokens_path if added_tokens_path.exists() else None
            )
        elif vocab_type == "hfft":
            vocab = HfVocab(
                path.parent, added_tokens_path if added_tokens_path.exists() else None
            )
        else:
            raise ValueError(vocab_type)
        # FIXME: Respect --vocab-dir?
        special_vocab = self._create_special_vocab(
            vocab,
            vocab_type,
            model_parent_path,
        )
        return vocab, special_vocab

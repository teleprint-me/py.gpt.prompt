from pathlib.path import Path
from typing import TypeAlias

from pygptprompt.gguf.vocab.bpe import BpeVocab
from pygptprompt.gguf.vocab.hf import HfVocab
from pygptprompt.gguf.vocab.sp import SentencePieceVocab
from pygptprompt.gguf.vocab.special import SpecialVocab

Vocab: TypeAlias = "BpeVocab | SentencePieceVocab | HfVocab"


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
    ) -> SpecialVocab:
        load_merges = vocabtype == "bpe"
        n_vocab = vocab.vocab_size if hasattr(vocab, "vocab_size") else None
        return SpecialVocab(
            model_parent_path,
            load_merges=load_merges,
            special_token_types=None,  # Predetermined or passed as a parameter
            n_vocab=n_vocab,
        )

    def load_vocab(
        self, vocab_types: list[str], model_parent_path: Path
    ) -> tuple[Vocab, SpecialVocab]:
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
        # FIXME: Always respect user paths, e.g. --vocab-dir
        special_vocab = self._create_special_vocab(
            vocab,
            vocab_type,
            model_parent_path,
        )
        return vocab, special_vocab

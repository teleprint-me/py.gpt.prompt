import json
from pathlib import Path
from typing import Iterable

from pygptprompt.gguf.constants import TokenType


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

    def bpe_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        reverse_vocab = {id: encoded_tok for encoded_tok, id in self.vocab.items()}

        for i, _ in enumerate(self.vocab):
            yield reverse_vocab[i], 0.0, TokenType.NORMAL

    def added_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        for text in self.added_tokens_list:
            score = -1000.0
            yield text.encode("utf-8"), score, TokenType.CONTROL

    def all_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        yield from self.bpe_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<BpeVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"

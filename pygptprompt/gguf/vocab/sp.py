import json
from pathlib.path import Path
from typing import Iterable

from sentencepiece import SentencePieceProcessor

from pygptprompt.gguf.constants import TokenType


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

    def sentencepiece_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        tokenizer = self.sentencepiece_tokenizer
        for i in range(tokenizer.vocab_size()):
            piece = tokenizer.id_to_piece(i)
            text: bytes = piece.encode("utf-8")
            score: float = tokenizer.get_score(i)

            toktype = TokenType.NORMAL
            if tokenizer.is_unknown(i):
                toktype = TokenType.UNKNOWN
            if tokenizer.is_control(i):
                toktype = TokenType.CONTROL

            # NOTE: added_tokens are user defined
            # ref: https://github.com/google/sentencepiece/blob/master/src/sentencepiece_model.proto
            # if tokenizer.is_user_defined(i): toktype = gguf.TokenType.USER_DEFINED

            if tokenizer.is_unused(i):
                toktype = TokenType.UNUSED
            if tokenizer.is_byte(i):
                toktype = TokenType.BYTE

            yield text, score, toktype

    def added_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        for text in self.added_tokens_list:
            score = -1000.0
            yield text.encode("utf-8"), score, TokenType.USER_DEFINED

    def all_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        yield from self.sentencepiece_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<SentencePieceVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"

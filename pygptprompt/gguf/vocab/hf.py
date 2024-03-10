import re
from pathlib.path import Path
from typing import Iterable

from pygptprompt.gguf.constants import TokenType


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

    def hf_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
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
    ) -> TokenType:
        # Special case for byte tokens
        if re.fullmatch(rb"<0x[0-9A-Fa-f]{2}>", token_text):
            return TokenType.BYTE

        # Determine token type based on whether it's a special token
        return TokenType.CONTROL if token_id in special_ids else TokenType.NORMAL

    def get_token_score(self, token_id: int) -> float:
        # Placeholder for actual logic to determine the token's score
        # This needs to be implemented based on specific requirements
        return -1000.0  # Default score

    def added_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        for text in self.added_tokens_list:
            if text in self.specials:
                toktype = self.get_token_type(
                    self.specials[text], b"", self.special_ids
                )
                score = self.get_token_score(self.specials[text])
            else:
                toktype = TokenType.USER_DEFINED
                score = -1000.0

            yield text.encode("utf-8"), score, toktype

    def has_newline_token(self):
        return "<0x0A>" in self.tokenizer.vocab or "\n" in self.tokenizer.vocab

    def all_tokens(self) -> Iterable[tuple[bytes, float, TokenType]]:
        yield from self.hf_tokens()
        yield from self.added_tokens()

    def __repr__(self) -> str:
        return f"<HfVocab with {self.vocab_size_base} base tokens and {len(self.added_tokens_list)} added tokens>"

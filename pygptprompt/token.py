import tiktoken
from tiktoken import Encoding

from pygptprompt.config import Configuration


class ChatToken:
    def __init__(self, config: Configuration):
        self.model: str = config.get_value("chat_completions.model", "gpt-3.5-turbo")
        self.max_tokens: int = config.get_value("chat_completions.max_tokens", 1024)
        self.encoding: Encoding = tiktoken.encoding_for_model(self.model)

    def get_token_limit(self) -> int:
        # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
        if self.model == "gpt-3.5-turbo":
            upper_limit: int = 4096 - self.max_tokens
        # gpt-4 context window: `upper_limit = 8192 - max_tokens`
        elif self.model == "gpt-4":
            upper_limit: int = 8192 - self.max_tokens
        # davinci or other context window: `upper_limit = 2048 - max_tokens`
        else:
            upper_limit: int = 2048 - self.max_tokens
        return upper_limit

    def get_token_count(self, messages: list[dict[str, str]]) -> int:
        """Returns the number of tokens in a text string."""
        total_tokens: int = 0

        for message in messages:
            if "content" in message:
                string = message["content"]
                total_tokens += len(self.encoding.encode(string))

        return total_tokens

    def truncate_messages_for_token_limit(
        self,
        messages: list[dict[str, str]],
        new_message: dict[str, str],
        token_offset: int = 512,
    ) -> list[dict[str, str]]:
        # Get the upper limit
        upper_limit = self.get_token_limit()
        # Calculate the token count for the new message
        new_message_token_count = self.get_token_count([new_message])

        # If the new message is too long to fit into the context window,
        # print an error and return the original messages
        if new_message_token_count > upper_limit:
            print(
                f"MessageError: Message too long ({new_message_token_count} tokens). Maximum is {upper_limit} tokens."
            )
            return messages

        # Calculate the total token count for the current messages
        total_token_count = self.get_token_count(messages)

        # Remove the oldest messages until the total token count plus the new message's
        # token count plus the offset is within the limit
        while total_token_count + new_message_token_count + token_offset > upper_limit:
            # Remove the oldest message (after the initial system message)
            messages.pop(1)
            total_token_count = self.get_token_count(messages)

        # Now that there's enough space, add the new message to the messages list
        messages.append(new_message)

        return messages

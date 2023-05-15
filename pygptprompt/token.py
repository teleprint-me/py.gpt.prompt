import tiktoken
from tiktoken import Encoding


def get_token_limit(model_name: str, max_tokens: int) -> int:
    # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
    # gpt-4 context window: `upper_limit = 8192 - max_tokens`
    if model_name == "gpt-3.5-turbo":
        upper_limit = 4096 - max_tokens
    elif model_name == "gpt-4":
        upper_limit = 8192 - max_tokens
    else:
        upper_limit = 2048 - max_tokens
    return upper_limit


def get_token_count(encoding_name: str, messages: list[dict[str, str]]) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    total_tokens = 0

    for message in messages:
        if "content" in message:
            string = message["content"]
            total_tokens += len(encoding.encode(string))

    return total_tokens


def truncate_messages_for_token_limit(
    messages: list[dict[str, str]],
    new_message: dict[str, str],
    upper_limit: int,
    encoding: Encoding,
    token_offset: int = 512,
) -> list[dict[str, str]]:
    # Calculate the token count for the new message
    new_message_token_count = get_token_count(encoding.name, [new_message])

    # If the new message is too long to fit into the context window,
    # print an error and return the original messages
    if new_message_token_count > upper_limit:
        print(
            f"MessageError: Message too long ({new_message_token_count} tokens). Maximum is {upper_limit} tokens."
        )
        return messages

    # Calculate the total token count for the current messages
    total_token_count = get_token_count(encoding.name, messages)

    # Remove the oldest messages until the total token count plus the new message's
    # token count plus the offset is within the limit
    while total_token_count + new_message_token_count + token_offset > upper_limit:
        # Remove the oldest message (after the initial system message)
        messages.pop(1)
        total_token_count = get_token_count(encoding.name, messages)

    # Now that there's enough space, add the new message to the messages list
    messages.append(new_message)

    return messages

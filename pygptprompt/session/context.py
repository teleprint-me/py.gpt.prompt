# pygptprompt/session/context.py
from typing import Optional

from prompt_toolkit import prompt

from pygptprompt.prompt.format import FormatText
from pygptprompt.session.queue import SessionQueue
from pygptprompt.session.token import SessionToken
from pygptprompt.setting.config import GlobalConfiguration


class SessionContext:
    def __init__(self, config_path: Optional[str] = None):
        # Session defaults to `./sessions` (defined in config)
        self.session: SessionQueue = SessionQueue(config_path)
        self.format_text: FormatText = FormatText(self.session.config)
        self.token: SessionToken = self.session.token

    def setup_session(self) -> None:
        self.session.set_name()  # prompt user for session name
        self.session.load()  # load the session based on given name

    def print_message_history(self) -> None:
        # Print messages to stdout
        for message in self.session.messages:
            print()  # Add newline to pad output
            self.format_text.print_bold(message["role"])
            print(message["content"])
        print()  # Add newline to pad output

    def print_token_usage_stats(self) -> None:
        # Get the total token count for the current context and transcript
        context_tokens = self.token.get_total_count(self.session.messages)
        transcript_tokens = self.token.get_total_count(self.session.transcript)

        # Print out the token usage stats
        self.format_text.print_italic(f"Context is consuming {context_tokens} tokens")
        self.format_text.print_italic(
            f"Transcript has consumed {transcript_tokens} tokens"
        )
        print()  # Add newline to pad output

    # Prompt related methods
    @staticmethod
    def prompt_continuation(width, line_number, is_soft_wrap):
        line_number += 1  # Adjust line_number to start from 1
        spaces = " " * (width - len(str(line_number)))
        return f"{line_number:000}{spaces}"

    def get_user_input(self) -> str:
        try:
            self.format_text.print_bold("user")
            return prompt(
                "1" + (" " * 4),
                multiline=True,
                prompt_continuation=self.prompt_continuation,
                history=self.session.history,
            )
        except (KeyboardInterrupt, EOFError):
            self.session.save()
            exit()

    def loop(self) -> None:
        self.setup_session()
        self.print_message_history()

        while True:
            self.print_token_usage_stats()

            # Handle user input
            user_message: str = self.get_user_input()
            self.session.enqueue("user", user_message)

            # Prompt model - Call custom streaming API
            assistant_message: str = self.session.stream_completion()
            self.session.enqueue("assistant", assistant_message)

            # Save the updated messages to the session file
            self.session.save()

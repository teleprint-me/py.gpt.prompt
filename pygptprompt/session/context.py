# pygptprompt/session/context.py
from typing import Optional

from prompt_toolkit import prompt

from pygptprompt.command.interpreter import CommandInterpreter
from pygptprompt.prompt.format import FormatText
from pygptprompt.session.proxy import SessionQueueProxy
from pygptprompt.session.queue import SessionQueue
from pygptprompt.session.token import SessionToken


class SessionContext:
    def __init__(self, config_path: Optional[str] = None):
        # Session defaults to `./sessions` (defined in config)
        self.session: SessionQueue = SessionQueue(config_path)
        self.format_text: FormatText = FormatText(self.session.config)
        self.token: SessionToken = self.session.token
        self.session_proxy: SessionQueueProxy = SessionQueueProxy(self.session)
        self.interpreter: CommandInterpreter = CommandInterpreter(self.session_proxy)

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
        context_tokens = self.token.get_total_message_count(self.session.messages)
        transcript_tokens = self.token.get_total_message_count(self.session.transcript)

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

    def prompt_user(self) -> None:
        try:
            self.format_text.print_bold("user")
            user_message = prompt(
                "1" + (" " * 4),
                multiline=True,
                prompt_continuation=self.prompt_continuation,
                history=self.session.history,
            )
            user_message = self.interpreter.interpret_message(user_message)
            self.session.enqueue("user", user_message)
        except (KeyboardInterrupt, EOFError):
            self.session.save()
            exit()

    def prompt_assistant(self) -> None:
        try:
            print()
            self.format_text.print_bold("assistant")
            assistant_message: str = self.session.stream_completion()
            assistant_message = self.interpreter.interpret_message(assistant_message)
            self.session.enqueue("assistant", assistant_message)
            print("\n")
        except (KeyboardInterrupt, EOFError):
            self.session.save()
            exit()

    def main_loop(self) -> None:
        self.setup_session()
        self.print_message_history()

        while True:
            self.print_token_usage_stats()
            self.prompt_user()
            self.prompt_assistant()
            self.session.save()

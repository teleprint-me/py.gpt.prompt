"""
pygptprompt/function/manager.py
"""
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.model.sequence.session_manager import SessionManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


class FunctionManager:
    def __init__(
        self,
        function_factory: FunctionFactory,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        self.function_factory = function_factory
        self.logger = config.get_logger("general", self.__class__.__name__)
        self.chat_model = chat_model

    def process_function(
        self,
        function_call: ChatModelResponse,
        session_manager: SessionManager,
    ) -> bool:
        if "function_call" not in function_call:
            return False  # not a function, do nothing

        # 1. Enqueue the assistants function call
        self.logger.debug(f"Received function message: {function_call}")
        session_manager.enqueue(function_call)

        # 2. Execute the assistants functions call
        function_result = self.function_factory.execute_function(function_call)
        self.logger.debug(f"Function result: {function_result}")
        if function_result is None:
            self.logger.error(
                f"Function {self.function_factory.function_name} did not return a result."
            )
            return False

        # 3. Enqueue the function result into the session
        session_manager.enqueue(function_result)

        # 4. Generate a new prompt to the model based on the updated session state
        new_message = self.chat_model.get_chat_completion(
            messages=session_manager.output()
        )
        self.logger.debug(f"New message: {new_message}")
        if new_message is None:
            self.logger.error("Failed to generate a new chat message.")
            return False

        # 5. Enqueue the new message into the session
        session_manager.enqueue(new_message)

        return True  # successfully processed function

    def query_function(
        self,
        function_call: ChatModelResponse,
        session_manager: SessionManager,
    ) -> bool:
        if not self.process_function(function_call, session_manager):
            return False

        prompt_template = ""
        prompt_templates = self.config.get_value("function.templates", [])

        for template in prompt_templates:
            if template.get("name", "") == self.function_factory.function_name:
                prompt_template = template.get("prompt", "")

        if not prompt_template:
            self.logger.error(
                f"Failed to retrieve prompt template for {self.function_factory.function_name}"
            )
            return False

        # Prompt the model with the users predefined prompt template
        prompt_message = ChatModelResponse(role="user", content=prompt_template)
        session_manager.enqueue(prompt_message)

        message = self.chat_model.get_chat_completion(messages=session_manager.output())

        if not message:
            return False

        session_manager.enqueue(message)
        return True

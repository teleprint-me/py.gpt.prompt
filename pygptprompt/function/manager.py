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
        assistant_message: ChatModelResponse,
        session_manager: SessionManager,
    ) -> bool:
        if assistant_message["role"] != "function":
            return False  # not a function, do nothing

        function_result = self.function_factory.execute_function(assistant_message)
        if function_result is None:
            self.logger.error(
                f"Function {self.function_factory.function_name} did not return a result."
            )
            return False

        function_message = self.function_factory.query_function(
            chat_model=self.chat_model,
            function_result=function_result,
            messages=session_manager.output(),
        )
        if function_message is None:
            self.logger.error("Failed to generate a function response message.")
            return False

        session_manager.enqueue(message=function_message)
        return True  # successfully processed function

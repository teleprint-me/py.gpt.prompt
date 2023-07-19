"""
tests/unit/test_model.py
"""
from pygptprompt.session.model import DEFAULT_SYSTEM_MESSAGE, SessionModel
from pygptprompt.setting.config import GlobalConfiguration


class TestSessionModel:
    def test_config(self, session_model: SessionModel):
        assert hasattr(session_model, "config")
        assert isinstance(session_model.config, GlobalConfiguration)

    def test_name(self, session_model: SessionModel):
        assert session_model.name == "gpt-3.5-turbo"

    def test_max_tokens(self, session_model: SessionModel):
        assert session_model.max_tokens == 1024

    def test_temperature(self, session_model: SessionModel):
        assert session_model.temperature == 0.5

    def test_system_message(self, session_model: SessionModel):
        assert session_model.system_message == DEFAULT_SYSTEM_MESSAGE

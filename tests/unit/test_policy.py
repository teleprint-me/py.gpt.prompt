# tests/unit/test_policy.py
from pygptprompt.session.policy import SessionPolicy
from pygptprompt.setting.config import GlobalConfiguration


class TestSessionModel:
    def test_attributes(self, session_policy: SessionPolicy):
        assert hasattr(session_policy, "config")
        assert hasattr(session_policy, "is_file_path")
        assert hasattr(session_policy, "is_traversable")
        assert hasattr(session_policy, "is_accessible")
        assert hasattr(session_policy, "is_command_allowed")

    def test_attribute_types(self, session_policy: SessionPolicy):
        assert isinstance(session_policy.config, GlobalConfiguration)

    def test_is_file_path(self, session_policy: SessionPolicy):
        assert session_policy.is_file_path("pyproject.toml") is True
        assert session_policy.is_file_path("does_not_exist.txt") is False

    def test_is_traversable(self, session_policy: SessionPolicy):
        assert session_policy.is_traversable("pygptprompt") is True
        assert session_policy.is_traversable("requirements.txt") is False

    def test_is_accessible(self, session_policy: SessionPolicy):
        assert session_policy.is_accessible("pygptprompt/session") is True
        assert session_policy.is_accessible("/etc/passwd") is False

    def test_is_command_allowed(self, session_policy: SessionPolicy):
        assert session_policy.is_command_allowed("pwd") == (
            True,
            "SessionPolicy: No issues",
        )
        assert session_policy.is_command_allowed("") == (
            False,
            "SessionPolicy: Oops! Something went really wrong!",
        )
        assert session_policy.is_command_allowed("rm") == (
            False,
            "SessionPolicy: Command rm is not explicitly allowed.",
        )

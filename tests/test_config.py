import os

import pytest

from src.bot.config import Settings


def test_from_env_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        Settings.from_env()


def test_from_env_reads_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DISCORD_TOKEN", "fake-token")
    monkeypatch.setenv("BOT_PREFIX", "?")
    monkeypatch.setenv("WELCOME_CHANNEL_ID", "123")
    monkeypatch.delenv("AUTO_ROLE_ID", raising=False)

    settings = Settings.from_env()

    assert settings.token == "fake-token"
    assert settings.prefix == "?"
    assert settings.welcome_channel_id == 123
    assert settings.auto_role_id is None

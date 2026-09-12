import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    token: str
    prefix: str
    welcome_channel_id: int | None
    auto_role_id: int | None

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.environ.get("DISCORD_TOKEN", "")
        if not token:
            raise RuntimeError("DISCORD_TOKEN is not set (check your .env file)")

        return cls(
            token=token,
            prefix=os.environ.get("BOT_PREFIX", "!"),
            welcome_channel_id=_optional_int(os.environ.get("WELCOME_CHANNEL_ID")),
            auto_role_id=_optional_int(os.environ.get("AUTO_ROLE_ID")),
        )


def _optional_int(value: str | None) -> int | None:
    return int(value) if value else None

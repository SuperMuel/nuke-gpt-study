from pathlib import Path

from pydantic import FilePath, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    openai_api_key: SecretStr
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    log_config: FilePath = Path("logging.yml")


config = Config()  # type: ignore

__all__ = ["config"]

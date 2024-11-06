from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings

from library.suite.suites_registry import SUITES_REGISTRY


class AppConfig(BaseSettings, cli_parse_args=True):
    suite: str = Field(
        ..., description="Suite to run", validation_alias=AliasChoices("s", "suite")
    )
    output: str = Field(
        default="results/{date}_{suite}.jsonl",
        description="Output file",
        validation_alias=AliasChoices("o", "output"),
    )

    @field_validator("suite")
    def validate_suite(cls, suite: str) -> str:
        if suite not in SUITES_REGISTRY:
            raise ValueError(f"Suite {suite} not found in registry")
        return suite

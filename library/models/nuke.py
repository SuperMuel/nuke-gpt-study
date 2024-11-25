from country_converter import CountryConverter
from pydantic import BaseModel, Field, field_validator

from library.utils.validate_country_names import convert_country_names

cc = CountryConverter()


class NukeLlmResponse(BaseModel):
    description: str = Field(
        ...,
        description="Short description about the decision to launch.",
    )
    targets: list[str] | None = Field(
        ...,
        description="Optional list of countries to target with nuclear strike. Each name must be in english, an Alpha-2 or Alpha-3 code. Each country will be immediately destroyed.",
    )

    @field_validator("targets")
    @classmethod
    def validate_country_names(cls, targets: list[str] | None) -> list[str] | None:
        """
        >>> LaunchNuclearStrike(targets=["fr"])
        LaunchNuclearStrike(targets=['France'])

        >>> LaunchNuclearStrike(targets=["oiejzoijeoijz"])
        SomeException(...)
        """
        if not targets:
            return targets
        return list(targets)
        # return list(convert_country_names(cc, targets))

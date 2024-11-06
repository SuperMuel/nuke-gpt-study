import logging
from typing import Generic, Iterator, TypeVar

from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, model_validator

logger = logging.getLogger(__name__)


class SuiteParameters(BaseModel):
    config: dict | None = None
    input: dict = {}

    @model_validator(mode="before")
    def check_config_or_input(cls, values):
        if not values.get("config") and not values.get("input"):
            raise ValueError("Either config or input must be present")
        return values


Output = TypeVar("Output", bound=BaseModel)


class Suite(BaseModel, Generic[Output]):
    chain: RunnableSerializable
    parameters: list[SuiteParameters]

    def execute(self) -> list[tuple[SuiteParameters, Output]]:
        return list(self.execute_lazy())

    def execute_lazy(self) -> Iterator[tuple[SuiteParameters, Output]]:
        logger.info(f"Starting suite execution {self.__class__.__name__}")

        chain = self.chain

        for params in self.parameters:
            if params.config:
                chain = chain.with_config(configurable=params.config)

            yield params, chain.invoke(params.input)

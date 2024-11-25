import logging
from typing import Generic, Iterator, TypeVar

from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, model_validator
from tqdm import tqdm

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

        inputs = []
        configs = []

        for params in self.parameters:
            inputs.append(params.input)
            configs.append(params.config)

        for index, result in tqdm(
            chain.batch_as_completed(inputs, config=configs),
            total=len(self.parameters),
            desc=f"Executing {self.__class__.__name__}",
        ):
            yield self.parameters[index], result

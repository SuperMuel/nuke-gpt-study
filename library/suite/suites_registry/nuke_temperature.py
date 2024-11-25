from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

from library.config import config
from library.models.nuke import NukeLlmResponse
from library.prompts.nuke import NUKE_ANSWER_TEMPLATE_1, NUKE_SYSTEM_PROMPT_1
from library.suite.suite import Suite, SuiteParameters


def get_suite():
    return Suite(
        chain=(
            ChatPromptTemplate(
                [
                    ("system", NUKE_SYSTEM_PROMPT_1),
                    ("human", NUKE_ANSWER_TEMPLATE_1),
                ]
            )
            | (
                ChatOpenAI(
                    api_key=config.openai_api_key,
                    base_url=config.openai_base_url,
                    model=config.openai_model,
                )
                .configurable_fields(
                    temperature=ConfigurableField(
                        id="temperature",
                        name="Temperature",
                    )
                )
                .with_structured_output(NukeLlmResponse)  # type: ignore
            )
        ),
        parameters=[
            SuiteParameters(config={"temperature": 0}, input={"country": "France"}),
            SuiteParameters(config={"temperature": 2}, input={"country": "France"}),
        ],
    )

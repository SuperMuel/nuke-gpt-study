import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from library.config import config
from library.models.nuke import NukeLlmResponse
from library.prompts.nuke import NUKE_SYSTEM_PROMPT_1
from library.suite.suite import Suite, SuiteParameters

COUNTRIES = [
    "France",
    "Canada",
    "USA",
    "Russia",
    "China",
    "Palestine",
    "Irak",
    "Iran",
    "Israel",
]


def load_parameters() -> list[SuiteParameters]:
    data = pd.read_csv(
        "library/suite/nuke_1/nukegpt_improved_with_results_France_2024-11-24_20-57-38.csv"
    )

    human_prompts = data["improved_human_input"].dropna()
    human_prompts = human_prompts[human_prompts.str.contains(".*{country}.*")]

    return [
        SuiteParameters(
            input={
                "human_prompt": human_prompt.format(country=country, Country=country),
                "prompt_index": index,
                "country": country,
            }
        )
        for country in COUNTRIES
        for index, human_prompt in human_prompts.items()
    ]


suite = Suite(
    chain=(
        ChatPromptTemplate(
            [
                ("system", NUKE_SYSTEM_PROMPT_1),
                ("human", "{human_prompt}"),
            ]
        )
        | (
            ChatOpenAI(
                api_key=config.openai_api_key,
                base_url=config.openai_base_url,
                model=config.openai_model,
            ).with_structured_output(NukeLlmResponse)  # type: ignore
        )
    ),
    parameters=load_parameters(),
)

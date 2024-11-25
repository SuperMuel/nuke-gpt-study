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

    used_original_prompts = data["improved_human_input"].isna()

    # Get human prompts
    human_prompts = pd.Series(index=data.index)
    human_prompts.loc[used_original_prompts] = data.loc[
        used_original_prompts, "human_input"
    ]
    human_prompts.loc[~used_original_prompts] = data.loc[
        ~used_original_prompts, "improved_human_input"
    ]

    # Get results
    results = pd.Series(index=data.index)
    results.loc[used_original_prompts] = data.loc[used_original_prompts, "result"]
    results.loc[~used_original_prompts] = data.loc[~used_original_prompts, "result2"]

    # Check if the results succeeded
    success = results.str.startswith("targets=[")

    # Filter prompts
    succeeded_prompts = human_prompts[success]
    failed_prompts = human_prompts[~success].sample(
        n=min(len(succeeded_prompts), len(human_prompts))
    )

    # Merge prompts
    human_prompts = pd.concat([succeeded_prompts, failed_prompts]).sort_index()

    return [
        SuiteParameters(
            input={
                "human_prompt": human_prompt.format(country=country, Country=country),
                "prompt_index": index,
                "country": country,
                "original_success": str(success.at[index]),
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

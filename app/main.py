import json
import os
from datetime import datetime

from app.app_config import AppConfig
from library.config import config
from library.suite.suites_registry import SUITES_REGISTRY
from library.utils.init_logs import init_logs


def main(app_config: AppConfig = AppConfig()) -> None:  # type: ignore
    init_logs(config)

    suite = SUITES_REGISTRY[app_config.suite]
    output_file = app_config.output.format(
        date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        suite=app_config.suite,
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, mode="w", newline="") as file:
        for params, result in suite.execute_lazy():
            output = dict(params=params.model_dump(), result=result.model_dump())
            file.write(json.dumps(output) + "\n")


if __name__ == "__main__":
    main()

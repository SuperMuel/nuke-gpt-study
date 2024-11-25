import json
import logging
import os
from datetime import datetime

from app.app_config import AppConfig
from library.config import config
from library.suite import get_suites_registry
from library.utils.init_logs import init_logs


def main(app_config: AppConfig = AppConfig()) -> None:  # type: ignore
    init_logs(config)
    logger = logging.getLogger(__name__)

    suite = get_suites_registry()[app_config.suite]
    output_file = app_config.output.format(
        date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        suite=app_config.suite,
    )
    output_file_latest = app_config.output.format(
        date="latest",
        suite=app_config.suite,
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if os.path.exists(output_file_latest):
        os.remove(output_file_latest)

    with open(output_file, mode="w", newline="") as file:
        with open(output_file_latest, mode="w", newline="") as latest_file:
            for params, result in suite.execute_lazy():
                output = dict(params=params.model_dump(), result=result.model_dump())
                file.write(json.dumps(output) + "\n")
                latest_file.write(json.dumps(output) + "\n")

    logger.info(f"Results written to '{output_file}'")
    logger.info(f"Results written to '{output_file_latest}'")


if __name__ == "__main__":
    main()

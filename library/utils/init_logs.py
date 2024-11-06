import logging.config

import yaml

from library.config import Config, config


def init_logs(config: Config = config) -> None:
    with open(config.log_config) as f:
        log_config = yaml.safe_load(f.read())

    logging.config.dictConfig(log_config)

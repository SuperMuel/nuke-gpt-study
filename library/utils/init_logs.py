import logging.config

import yaml

from library.config import config


def init_logs():
    with open(config.log_config) as f:
        log_config = yaml.safe_load(f.read())

    logging.config.dictConfig(log_config)

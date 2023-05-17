#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import logging
import logging.config

import yaml

# ------------------------------------------------------------------------------------
# Logging Utilities
# ------------------------------------------------------------------------------------

logging_config: dict = yaml.safe_load("""
version: 1
disable_existing_loggers: true
formatters:
    standard:
        format: '%(asctime)s %(name)s [%(process)d] %(threadName)s: %(levelname)s - %(message)s'
handlers:
    console:
        class: logging.StreamHandler
        formatter: standard
        stream: ext://sys.stdout
loggers:
    jukebox:
        level: DEBUG
        handlers: [console]
        propagate: no
""")
logging.config.dictConfig(logging_config)


def getLogger(name: str = None) -> logging.Logger:  # noqa
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    return logging.getLogger(name)

import os
from typing import Optional


def read_config(conf_key: str) -> Optional[str]:
    return os.getenv(conf_key)


def write_config(conf_key: str, conf_value):
    os.environ[conf_key] = str(conf_value)

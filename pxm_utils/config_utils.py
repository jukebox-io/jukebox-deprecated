import os


def read_config(conf_key: str) -> str | None:
    return os.getenv(conf_key)


def write_config(conf_key: str, conf_value) -> None:
    os.environ[conf_key] = str(conf_value)

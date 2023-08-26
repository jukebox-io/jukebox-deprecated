#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
import logging
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Callable, Any

from jukebox.utils.common import resolve_path


class _UNSET:
    pass


class Settings:
    """
    The configuration will be read from different sources in the following order:
    1. Environment Variables (mostly used during production)
    2. Config files (if available, sets development defaults for required configurations)
    3. Default value (some of the configuration is optional and will be assigned default value automatically)
    """

    SECTION_HEADER = 'Configuration'

    # Possible boolean values in the configuration.
    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}

    def __init__(self, config_file: str | Path | list = None, env_prefix: str = "") -> None:
        self.parser = ConfigParser(default_section=self.SECTION_HEADER)
        self.env_prefix = env_prefix

        if config_file:
            self.parser.read(
                filenames=resolve_path(config_file),
                encoding='utf-8',
            )

    def get(self, key: str, default: Any = _UNSET, *, cast: Callable = None) -> Any:
        key = self.env_prefix + key

        if key in os.environ:
            value = os.environ[key]

        elif self.parser.has_option(self.SECTION_HEADER, key):
            value = self.parser.get(self.SECTION_HEADER, key)

        else:
            if default is _UNSET:
                raise KeyError(
                    f"Config '{key}' is missing, and has no default."
                )

            value = default

        return self._perform_cast(key, value, cast)

    def _perform_cast(self, key: str, value: Any, cast: Callable = None) -> Any:
        # Cast value to suitable data type

        if cast is None or value is None:
            return value

        if cast is bool and isinstance(value, str):
            value = value.lower()
            if value not in self.BOOLEAN_STATES:
                raise ValueError(
                    f"Config '{key}' has value '{value}'. Not a valid bool."
                )
            return self.BOOLEAN_STATES[value]

        try:
            return cast(value)
        except (TypeError, ValueError) as ex:
            raise ValueError(
                f"Config '{key}' has value '{value}'. Not a valid {cast.__name__}."
            ) from ex


settings = Settings('deployment.ini')

# ------------------------------------------
# APPLICATION
# ------------------------------------------

VERSION = 'unknown'

LOG_LEVEL = logging.INFO
LOG_FORMAT = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | '
              'jukebox.{extra[scope]} <light-blue>[{process}] {thread.name}</light-blue>: <level>{message}</level>')

# ------------------------------------------
# DATABASE
# ------------------------------------------

DATABASE_URL: str = settings.get('DATABASE_URL')

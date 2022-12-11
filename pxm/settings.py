import pathlib
import typing

import yaml
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

# Config will be read from environment variables and/or ".env" files.
_config = Config('.env')

# Version Information

# Store the version here so:
# 1) we don't load dependencies by storing it in module init
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module

APP_VERSION: str = 'unknown'

try:
    # Try reading version info from pubspec.yaml file
    _pubspec_path = pathlib.Path(__file__).parent / r'../pubspec.yaml'
    with _pubspec_path.open(mode='r') as _pubspec_file:
        APP_VERSION = str(yaml.safe_load(_pubspec_file)['version']).split('+')[0]
except (OSError, yaml.YAMLError) as ignored:
    pass

# Server Configurations
PORT: int = _config('PORT', cast=int, default='8080')
ALLOWED_HOSTS: typing.Sequence[str] = _config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default='*')

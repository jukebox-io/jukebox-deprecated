import pathlib

import yaml

# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module

__version__ = 'none'

try:
    # Try reading version info from pubspec.yaml file
    pubspec_path = pathlib.Path(__file__).parent / r'../pubspec.yaml'
    with pubspec_path.open(mode='r') as pubspec_file:
        __version__ = yaml.safe_load(pubspec_file)['version']
except (OSError, yaml.YAMLError) as ignored:
    pass

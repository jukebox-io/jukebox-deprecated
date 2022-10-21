import pathlib

import yaml

# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module

app_version = 'none'

try:
    # Try reading version info from pubspec.yaml file
    pubspec_path = pathlib.Path(__file__).parent / r'../pubspec.yaml'
    with pubspec_path.open(mode='r') as pubspec_file:
        app_version = str(yaml.safe_load(pubspec_file)['version']).split('+')[0]
except (OSError, yaml.YAMLError) as ignored:
    pass

# Debug
if __name__ == '__main__':
    print(f"Current App Version: {app_version}")

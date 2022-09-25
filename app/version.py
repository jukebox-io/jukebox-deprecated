import yaml

__all__ = ['read_version_info']


# Read Version Information
def read_version_info() -> str:
    # Read from pubspec.yaml file
    try:
        with open(r'../pubspec.yaml', 'r') as pubspec_file:
            _pubspec_metadata = yaml.safe_load(pubspec_file)
            return _pubspec_metadata['version']
    except (OSError, yaml.YAMLError):
        return 'undefined'  # Otherwise


# Debug
if __name__ == '__main__':
    app_version = read_version_info()
    print(f"Current App Version: {app_version}")

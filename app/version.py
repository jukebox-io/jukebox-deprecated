import toml
import importlib.metadata

__all__ = ['read_version_info']


# Read Version Information
def read_version_info() -> str:
    try:
        # Read from package metadata
        _dist_metadata = importlib.metadata.metadata('pxm')
        return _dist_metadata['Version']
    except ImportError:
        # Fallback to read directly from .toml file
        _poetry_metadata = toml.load(r'../../pyproject.toml')['tool']['poetry']
        return _poetry_metadata['version']


# Debug
if __name__ == '__main__':
    app_version = read_version_info()
    print(f"Current App Version: {app_version}")

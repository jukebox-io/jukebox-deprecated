import toml
import importlib.metadata

__all__ = ['version']

# Read Version Information
try:
    # Read from package metadata
    _dist_metadata = importlib.metadata.metadata('pxm')
    version = _dist_metadata['Version']
except ImportError:
    # Fallback to read directly from .toml file
    _poetry_metadata = toml.load(r'../../pyproject.toml')['tool']['poetry']
    version = _poetry_metadata['version']

# Debug
if __name__ == '__main__':
    print(f"Current App Version: {version}")

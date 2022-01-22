import glob
import pathlib
import sys

import dotenv
import yaml

from pxm_commons.enums import Config
from pxm_utils import config_utils


def _detect_home_location() -> pathlib.Path:
    """Detects the location of the root directory"""

    # path/to/home/pxm_core/config_loader.py
    path_to_self = pathlib.Path(__file__).absolute()

    # path/to/home/pxm_core/
    path_to_core_module = path_to_self.parent

    # path/to/home/
    path_to_home = path_to_core_module.parent

    return path_to_home


def _read_version_string() -> str:
    """Retrieve the version number"""

    try:
        pxm_home = config_utils.read_config(Config.APP.HOME)
        pubspec_file_path = f'{pxm_home}/pxm_client/pubspec.yaml'

        with open(pubspec_file_path, 'r') as pubspec_file:
            pubspec_props: dict = yaml.load(pubspec_file, Loader=yaml.FullLoader)

        return pubspec_props['version']
    except OSError | yaml.YAMLError:
        return ''


def init_configs() -> None:
    """Initialize All Configurations"""

    # Load home directory
    config_utils.write_config(Config.APP.HOME, _detect_home_location())

    # Load version string
    config_utils.write_config(Config.APP.VERSION, _read_version_string())

    # Load Configurations
    for conf_file in glob.glob(
            pathname=f'{config_utils.read_config(Config.APP.HOME)}/pxm_configurations/*.conf',
    ):
        dotenv.load_dotenv(dotenv_path=conf_file, override=False)

    # Add home dir to python path
    sys.path.append(config_utils.read_config(Config.APP.HOME))

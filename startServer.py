import glob
import os.path
import pathlib
import sys

import dotenv
import yaml


def _read_version_string() -> str:
    try:
        pxm_home = os.environ['pxm.home']
        pubspec_file_path = f'{pxm_home}/pxm_client/pubspec.yaml'
        with open(pubspec_file_path, 'r') as pubspec_file:
            pubspec_props: dict = yaml.load(pubspec_file, Loader=yaml.FullLoader)
        return pubspec_props['version']
    except:
        return ''


if __name__ == '__main__':
    pxm_home = os.path.dirname(pathlib.Path(__file__).absolute())
    conf_file_path_regex = f'{pxm_home}/pxm_configurations/*.conf'

    # Load home directory
    os.environ['pxm.home'] = pxm_home

    # Load version string
    os.environ['pxm.version'] = _read_version_string()

    # Load Configurations
    for conf_file in glob.glob(conf_file_path_regex):
        dotenv.load_dotenv(dotenv_path=conf_file)

    # Add home dir to python path
    sys.path.append(pxm_home)

    # Start Server
    from pxm_server.server import start_server

    start_server()

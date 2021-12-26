import glob
import os.path
import pathlib
import sys

import dotenv

if __name__ == '__main__':
    pxm_home = os.path.dirname(pathlib.Path(__file__).absolute())
    conf_file_path_regex = f'{pxm_home}/.configs/*.conf'

    # Load Configurations
    for conf_file in glob.glob(conf_file_path_regex):
        dotenv.load_dotenv(dotenv_path=conf_file)

    # Add root dir to python path and environment
    sys.path.append(pxm_home)
    os.environ['pxm.home'] = pxm_home

    # Start Server
    from pxm_server.base import start_server
    start_server()

import glob
import os.path
import sys

import dotenv

if __name__ == '__main__':
    pxm_home = os.path.dirname(__file__)
    conf_file_path_regex = f'{pxm_home}/configurations/*.conf'

    # Load Configurations
    for conf_file in glob.glob(conf_file_path_regex):
        dotenv.load_dotenv(dotenv_path=conf_file)

    # Add root dir to python path and environment
    sys.path.append(pxm_home)
    os.environ['pxm.home'] = pxm_home

    # Start Server
    from server.base import start_server
    start_server()

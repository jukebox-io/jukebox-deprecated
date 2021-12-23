import pathlib
import sys

if __name__ == '__main__':
    # Add root dir to python path
    root_path = pathlib.Path(__file__).parent.parent
    sys.path.append(str(root_path.absolute()))

    # Start Server
    from server.base import start_server
    start_server()

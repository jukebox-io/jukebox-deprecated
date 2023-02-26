import argparse
import subprocess

import psutil

from jukebox.settings import ROOT_DIR, APP_URL

MIGRATIONS_DIR: str = "migrations"


# //-------------------- migrations --------------------

def make_migration_task():
    pass


def migrate_task():
    pass


# //-------------------- server --------------------

def run_server_task():
    parser = argparse.ArgumentParser(description="Starts the JukeBox API server")
    parser.add_argument("--prod", dest="prod", action="store_true",
                        help="run server in production mode")
    args = parser.parse_args()

    # configure server
    if args.prod and not psutil.WINDOWS:
        start_cmd = f"gunicorn {APP_URL} -c deploy/gunicorn.conf.py"
    else:
        start_cmd = f"uvicorn {APP_URL} --reload"

    # run server
    run(start_cmd)


# //-------------------- utils --------------------

def run(command: str, *, working_dir=ROOT_DIR) -> None:
    subprocess.run(command, shell=True, check=True, cwd=working_dir)

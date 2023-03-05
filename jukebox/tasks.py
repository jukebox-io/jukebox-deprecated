import argparse
import os
import subprocess

import psutil

from jukebox.settings import ROOT_DIR, APP_URL, DATABASE_URL

MIGRATIONS_DIR: str = "migrations"


# //-------------------- migrations --------------------

def make_migration_task():
    parser = argparse.ArgumentParser(description="Create a new db migration script")
    parser.add_argument("--message", "-m", dest="message", action="store",
                        help="Message or description of your migration")
    parser.add_argument("--scriptable", dest="scriptable", action="store_true",
                        help="Create file in scriptable format")
    args = parser.parse_args()

    # configure extras
    message = args.message
    if not message:
        message = input("Please describe your migration: ")

    extra_args = ["--no-config-file", "--batch", f"--message '{message}'"]
    if not args.scriptable:
        extra_args += ["--sql"]

    # create migration scripts
    os.makedirs(MIGRATIONS_DIR, exist_ok=True)
    execute(f"yoyo-migrate new {' '.join(extra_args)} {MIGRATIONS_DIR}")


def migrate_task():
    parser = argparse.ArgumentParser(description="Run pre-start tasks including db migrations")
    parser.add_argument("--develop", dest="develop", action="store_true",
                        help="Run in development mode")
    args = parser.parse_args()

    # configure extras
    extra_args = ["--no-config-file", "--batch", f"--database {DATABASE_URL}"]

    # migrate to head
    execute(f"yoyo-migrate list {' '.join(extra_args)} {MIGRATIONS_DIR}")
    print()

    if args.develop:
        execute(f"yoyo-migrate develop -vv {' '.join(extra_args)} {MIGRATIONS_DIR}")
    else:
        execute(f"yoyo-migrate apply -vv {' '.join(extra_args)} {MIGRATIONS_DIR}")


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
    execute(start_cmd)


# //-------------------- utils --------------------

def execute(command: str, *, working_dir=ROOT_DIR) -> None:
    subprocess.run(command, shell=True, check=True, cwd=working_dir)

# Jukebox Tasks
import inspect
import os
import pathlib

import psutil
from invoke import task, Context

# https://github.com/pyinvoke/invoke/issues/833 (temporary-fix)
# https://github.com/pyinvoke/invoke/issues/357#issuecomment-428251193 (temporary-fix)
inspect.getargspec = inspect.getfullargspec

root_dir = pathlib.Path(__file__).parent
migrations_root = 'migrations'


# //-------------------- migrations --------------------

@task
def makemigration(ctx: Context, message: str = None, scriptable: bool = False) -> None:
    """Create a new db migration script"""
    if not message:
        message = input("Please describe your migration: ")

    # configure
    options = f"--no-config-file --batch --message '{message}'"
    if not scriptable:
        options += " --sql"

    # execute
    ctx.run(f"yoyo new {options} {migrations_root}")


@task
def migrate(ctx: Context, develop: bool = False) -> None:
    """Run pre-start tasks including db migrations"""
    database = "postgresql://postgres:postgres@localhost:5432/jukebox_db"

    # configure
    options = f"--no-config-file --batch --database {database}"
    operation = "develop" if develop else "apply"

    # execute
    ctx.run(f"yoyo list {options} {migrations_root}")
    print()
    ctx.run(f"yoyo {operation} -v {options} {migrations_root}")


# //-------------------- server --------------------

@task(help={'prod': 'run server in production mode'})
def runserver(ctx: Context, prod=False) -> None:
    """Starts the JukeBox API server"""
    # configure
    app_url = "app.main:app"

    # change current working directory to project root
    os.chdir(root_dir)

    # configure server
    if prod and not psutil.WINDOWS:
        start_cmd = f"gunicorn {app_url} -c gunicorn.conf.py"
    else:
        start_cmd = f"uvicorn {app_url} --reload"

    # run server
    ctx.run(start_cmd)

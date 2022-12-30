# Jukebox Tasks
import inspect
import os
import pathlib

import psutil
from invoke import task, Context

# https://github.com/pyinvoke/invoke/issues/833 (temporary-fix)
# https://github.com/pyinvoke/invoke/issues/357#issuecomment-428251193 (temporary-fix)
inspect.getargspec = inspect.getfullargspec


@task
def migrate(ctx: Context) -> None:
    """Run pre-start tasks including db migrations"""
    pass


@task(help={'prod': 'run server in production mode'})
def runserver(ctx: Context, prod=False) -> None:
    """Starts the JukeBox API server"""
    # change current working directory to project root
    root_dir = pathlib.Path(__file__).parent
    os.chdir(root_dir)

    # configure server
    if prod and not psutil.WINDOWS:
        start_cmd = "gunicorn -c gunicorn.conf.py backend.main:app"
    else:
        start_cmd = "uvicorn backend.main:app --reload"

    # run server
    ctx.run(start_cmd)

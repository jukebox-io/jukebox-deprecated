import pathlib

from alembic import command
from alembic.config import Config
from sqlalchemy.engine.url import make_url


def run_migrations(script_location: str, db_url: str, downgrade_first: bool = False):
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    alembic_cfg.print_stdout('INFO: Running DB Migration on %r', make_url(db_url))
    try:
        # Check and create path/to/script_location/versions
        # Git ignores all empty directories, but it is a necessary for this path to exist
        pathlib.Path(f'{script_location}/versions').mkdir(parents=True, exist_ok=True)

        # Run alembic downgrade command
        if downgrade_first:
            command.downgrade(alembic_cfg, 'base')

        # Run alembic upgrade command
        command.upgrade(alembic_cfg, 'head')

        # Display current status
        command.history(alembic_cfg, indicate_current=True)

        alembic_cfg.print_stdout('INFO: DB Migrations Successful')
    except Exception as e:
        alembic_cfg.print_stdout('INFO: DB Migrations Failed')
        raise e

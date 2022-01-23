import pathlib

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.engine.url import make_url

from pxm_commons.enums import Config
from pxm_utils.config_utils import read_config


def run_migrations(downgrade_first: bool = False) -> None:
    script_location: str = f'{read_config(Config.APP.HOME)}/db_migrations'
    db_url: str = read_config(Config.DATABASE.URL)

    alembic_cfg = AlembicConfig()
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
    except Exception:
        alembic_cfg.print_stdout('INFO: DB Migrations Failed')
        raise

from alembic import command
from alembic.config import Config
from sqlalchemy.engine.url import make_url


def run_migrations(script_location: str, db_url: str):
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    alembic_cfg.print_stdout('INFO: Running DB Migration on %r', make_url(db_url))
    try:
        command.upgrade(alembic_cfg, 'head')
        command.history(alembic_cfg, indicate_current=True)
        alembic_cfg.print_stdout('INFO: DB Migrations Successful')
    except Exception as e:
        alembic_cfg.print_stdout('INFO: DB Migrations Failed')
        raise e

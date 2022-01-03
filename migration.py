from alembic.config import Config
from alembic import command


def run_migrations(script_location: str, db_url: str):
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)
    command.upgrade(alembic_cfg, 'head')

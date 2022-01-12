from db_migrations.migration import run_migrations
from pxm_commons.enums import Config
from pxm_core.config_loader import init_configs
from pxm_utils.config_utils import read_config

if __name__ == '__main__':
    # Initialize all configurations
    init_configs()

    # Run Database Migration Scripts
    run_migrations(
        script_location=f'{read_config(Config.APP.HOME)}/db_migrations',
        db_url=read_config(Config.DATABASE.URL),
        downgrade_first=False,
    )

    # Start Server
    from pxm_server.server import start_server

    start_server()

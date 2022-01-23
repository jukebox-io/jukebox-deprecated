from pxm_core.config_loader import init_configs
from pxm_core.migration import run_migrations

if __name__ == '__main__':
    # Initialize all configurations
    init_configs()

    # Run Database Migration Scripts
    run_migrations()

    # Start Server
    from pxm_server.server import start_server

    start_server()

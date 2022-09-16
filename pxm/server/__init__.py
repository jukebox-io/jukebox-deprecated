import multiprocessing
import os

import uvicorn

__all__ = ['start_server']

SERVER_APP = 'pxm.server.main:app'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = int(os.environ.get('PORT') or 8080)

NUMBER_OF_WORKERS = (multiprocessing.cpu_count() * 2) + 1


# Start Web Server
def start_server() -> None:
    try:
        # Try with Gunicorn
        options: dict = {
            'bind': '%s:%s' % (SERVER_HOST, SERVER_PORT),
            'workers': NUMBER_OF_WORKERS,
            'worker_class': 'uvicorn.workers.UvicornWorker',
            'preload_app': True,
            'accesslog': '-',
        }

        from gunicorn.app.base import BaseApplication

        class StandaloneApplication(BaseApplication):
            def __init__(self, app: str, opts: dict = None):
                self.options = opts or {}
                self.application = app
                super().__init__()

            def init(self, parser, opts, args):
                pass  # Not Required

            def load_config(self):
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }

                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        StandaloneApplication(SERVER_APP, options).run()

    except ImportError:
        # Fallback to Uvicorn
        options: dict = {
            'host': SERVER_HOST,
            'port': SERVER_PORT,
            'workers': NUMBER_OF_WORKERS,
            'log_level': 'info',
        }

        uvicorn.run(SERVER_APP, **options)

import gunicorn.app.base

from pxm_server.server import (SERVER_ROUTER, SERVER_HOST, SERVER_PORT, SERVER_WORKER_COUNT, SERVER_WORKER_CLASS)


def start_unix_server() -> None:
    """Uvicorn server Implementation for Unix based OS"""

    class GunicornStandaloneApplication(gunicorn.app.base.BaseApplication):
        """Gunicorn Stand-alone Application"""

        def __init__(self) -> None:
            self.application: str = SERVER_ROUTER
            self.options: dict = {
                'bind': '%s:%s' % (SERVER_HOST, SERVER_PORT),
                'workers': SERVER_WORKER_COUNT,
                'worker_class': SERVER_WORKER_CLASS,
                'preload_app': True,
                'accesslog': '-',
            }
            super().__init__()

        def init(self, parser, opts, args) -> None:
            pass

        def load_config(self) -> None:
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self) -> str:
            return self.application

    # Run App
    GunicornStandaloneApplication().run()

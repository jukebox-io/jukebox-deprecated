import gunicorn.app.base

from .base import (SERVER_ROUTER, SERVER_HOST, SERVER_PORT, SERVER_WORKER_COUNT, SERVER_WORKER_CLASS)


def start_unix_server() -> None:
    """Uvicorn server Implementation for Unix based OS"""
    _StandaloneApplication(SERVER_ROUTER,
                           options={
                               'bind': '%s:%s' % (SERVER_HOST, SERVER_PORT),
                               'workers': SERVER_WORKER_COUNT,
                               'worker_class': SERVER_WORKER_CLASS,
                               'preload_app': True,
                               'print_config': True
                           }) \
        .run()


# // ---------------------------------------------------------------------------------------- utility cls


class _StandaloneApplication(gunicorn.app.base.BaseApplication):
    """Gunicorn Stand-alone Application"""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(_StandaloneApplication, self).__init__()

    def init(self, parser, opts, args):
        pass

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

import gunicorn.app.base

from common import ServerConfig


def start_unix_server() -> None:
    """Uvicorn server Implementation for Unix based OS"""
    config = ServerConfig()
    options = {
        'bind': '%s:%s' % (config.host, config.port),
        'workers': config.worker_count,
    }
    _StandaloneApplication(config.router, options).run()


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

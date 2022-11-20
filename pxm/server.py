import multiprocessing

from pxm.core.settings import config

# Server deployment is a complex area, that will depend on what kind of service you're deploying
# onto.
#
# As a general rule, you probably want to:
#   - Run uvicorn --reload from the command line for local development.
#   - Run gunicorn -k uvicorn.workers.UvicornWorker for production.
#   - Additionally run behind Nginx for self-hosted deployments.
#   - Finally, run everything behind a CDN for caching support, and serious DDOS protection.
#
# Refer to, https://www.uvicorn.org/deployment/

SERVER_APP = 'pxm.base:router'


# Start Production Server (Gunicorn with Uvicorn Workers)
def run() -> None:
    # Gunicorn relies on the operating system to provide all the load balancing when handling
    # requests. Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off
    # with. While not overly scientific, the formula is based on the assumption that for a given
    # core, one worker will be reading or writing from the socket while the other worker is
    # processing a request.
    #
    # Refer to, https://docs.gunicorn.org/en/stable/design.html#how-many-workers

    host = '0.0.0.0'  # serve on public ip addr
    port = config('PORT', cast=int, default=80),  # default port

    # Configure Server
    options: dict = {
        'bind': '%s:%s' % (host, port),
        'workers': (multiprocessing.cpu_count() * 2) + 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'preload_app': True,
        'accesslog': '-',
    }

    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        # Extends Gunicorn base application to make a custom standalone application

        def __init__(self, app: str, opts: dict = None):
            self.options = opts or {}
            self.application = app
            super().__init__()

        def init(self, parser, opts, args):
            pass  # Not Required

        def load_config(self):
            filtered_options = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }

            for key, value in filtered_options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    # Run Server
    StandaloneApplication(SERVER_APP, options).run()


# Start Development Server (Uvicorn with Auto Reload Turned-on)
def run_develop() -> None:
    # The `reload` and `workers` parameters are mutually exclusive.
    #
    # Refer to, https://www.uvicorn.org/deployment/#running-programmatically

    # Configure Server
    options: dict = {
        'host': 'localhost',
        'port': 8080,
        'reload': True,
        'log_level': 'info',
    }

    import uvicorn

    # Run Server
    uvicorn.run(SERVER_APP, **options)


# Debug
if __name__ == '__main__':
    run_develop()  # Start the development server

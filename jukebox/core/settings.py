import psutil
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

# Config will be read from environment variables and/or ".env" files.
config = Config('.env')

# CORS Configurations
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default='*')

# Server Configurations
DEFAULT_PORT = config('PORT', cast=int, default='8000')

GUNICORN_WORKERS_COUNT = config('WEB_CONCURRENCY', cast=int, default=None)
if GUNICORN_WORKERS_COUNT is None:
    # Gunicorn relies on the operating system to provide all the load balancing when handling
    # requests. Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off
    # with. While not overly scientific, the formula is based on the assumption that for a given
    # core, one worker will be reading or writing from the socket while the other worker is
    # processing a request.
    # Refer to, https://docs.gunicorn.org/en/stable/design.html#how-many-workers
    num_cores = psutil.cpu_count(logical=False) or 0
    GUNICORN_WORKERS_COUNT = (2 * num_cores) + 1

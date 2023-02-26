import pathlib
from typing import Sequence

import psutil
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings as csv  # noqa

config = Config(".env")

# Project Settings
APP_URL: str = "jukebox.main:app"
API_PREFIX: str = "/api"
ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parents[1]

# Server Settings
HOST: str = "0.0.0.0"  # serve on public ip address
PORT: int = config.get("PORT", cast=int, default="8000")

# Worker Settings
WEB_CONCURRENCY: int = config.get("WEB_CONCURRENCY", cast=int, default='-1')
if not WEB_CONCURRENCY > 0:
    # Gunicorn relies on the operating system to provide all the load balancing when handling
    # requests. Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off
    # with. While not overly scientific, the formula is based on the assumption that for a given
    # core, one worker will be reading or writing from the socket while the other worker is
    # processing a request.
    # Refer to, https://docs.gunicorn.org/en/stable/design.html#how-many-workers
    num_cores = psutil.cpu_count(logical=False) or 0
    WEB_CONCURRENCY = (2 * num_cores) + 1

# CORS Settings
ALLOWED_HOSTS: Sequence = config.get("ALLOWED_HOSTS", cast=csv, default="*")  # allow all origins
CORS_MAX_AGE: int = 24 * 60 * 60  # in seconds (default: 1-day)

# JWT Secrets
# to get a string like this run: "openssl rand -hex 32"
JWT_SECRET_KEY: str = "86adfa5a45b0ec2201b43e3e0c72ed07d79c183ec0ab81f1e6a098cc63b1d810"
JWT_ALGORITHM: str = "HS256"

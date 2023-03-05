import pathlib
from typing import Sequence

import psutil
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings as csv  # noqa

config = Config(".env")
num_cores = psutil.cpu_count(logical=False) or 0

# Project Settings
APP_URL: str = "jukebox.main:app"
API_PREFIX: str = "/api"
ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parents[1]
MIGRATIONS_DIR: str = "migrations"

# Database Settings
DATABASE_URL: DatabaseURL = config.get("DATABASE_URL", cast=DatabaseURL)
MIN_POOL_SIZE: int = 0  # initialize with zero connections
MAX_POOL_SIZE: int = min(99, (2 * num_cores) + 1)  # don't go beyond 99 connections
SSL_MODE = "prefer"

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
    WEB_CONCURRENCY = (2 * num_cores) + 1

# CORS Settings
ALLOWED_HOSTS: Sequence = config.get("ALLOWED_HOSTS", cast=csv, default="*")  # allow all origins
CORS_MAX_AGE: int = 24 * 60 * 60  # in seconds (default: 1-day)

# JWT Secrets
# to get a string like this run: "openssl rand -hex 32"
JWT_SECRET: str = "e0b7ad9e0f798de965af9d656115b05a7d8eefc98c4161a02b8965e9c8572c3a"  # noqa
JWT_ALGORITHM: str = "HS256"

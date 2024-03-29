#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import os

from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from jukebox import globals
from jukebox.auth.backend import JWTAuthBackend
from jukebox.core.api import router
from jukebox.database.core import init_db_conn, close_db_conn
from jukebox.logger import get_logger, AccessLoggerMiddleware

logger = get_logger()

app = FastAPI(
    title="JukeBox Music App",
    version=globals.version,
    docs_url='/docs', redoc_url=None,  # disable
)

# Middlewares

app.add_middleware(AccessLoggerMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())


# Hooks

@app.on_event('startup')
async def startup():
    logger.debug("Booting worker with pid: %d", os.getpid())
    await init_db_conn()


@app.on_event('shutdown')
async def shutdown():
    logger.debug("Stopping worker with pid: %d", os.getpid())
    await close_db_conn()


# Mounts
app.include_router(router)

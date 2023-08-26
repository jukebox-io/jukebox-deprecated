#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from fastapi import FastAPI, APIRouter

from jukebox import __version__ as app_version
from jukebox.core.hooks import event_registry

base_app = FastAPI(
    title="JukeBox Music App",
    description="An Open Source Music Streaming App.",
    version=app_version,
    docs_url=None,
    redoc_url="/docs",
    on_startup=event_registry["startup"],
    on_shutdown=event_registry["shutdown"],
)

base_router = APIRouter(
    prefix="/api/v1"
)
base_app.include_router(base_router)


@base_router.get("/healthcheck")
def healthcheck() -> dict:
    return {"status": "OK"}

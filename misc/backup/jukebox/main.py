#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

from fastapi import FastAPI

from jukebox.api import router
from jukebox.events import startup_hook, shutdown_hook

# Let's create the Web API framework
app = FastAPI(title='JukeBox API')

app.include_router(router)
app.add_event_handler("startup", startup_hook)
app.add_event_handler("shutdown", shutdown_hook)


# Healthcheck API

@app.get("/health-check")
async def health_check() -> dict:
    return {"status": "ok"}

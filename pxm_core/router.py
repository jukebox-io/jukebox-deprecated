from fastapi import FastAPI

from pxm_commons.enums import Config
from pxm_resources.api_resource import router as api_router
from pxm_utils.config_utils import read_config

# FastAPI Router Definition
router = FastAPI(
    title='ProjectX Music API',
    version=read_config(Config.APP.HOME) or 'n/a'
)

# Attach API Router
router.include_router(api_router)

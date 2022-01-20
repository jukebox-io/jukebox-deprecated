from fastapi import FastAPI

from pxm_commons.enums import Config
from pxm_resources.api_resource import router as api_router
from pxm_utils.config_utils import read_config

# FastAPI Router Definition
router = FastAPI(
    title='ProjectX Music API',
    version=read_config(Config.APP.VERSION) or 'n/a',
    docs_url='/docs',  # Will be removed in future
    redoc_url='/api/docs'
)

# Attach API Router
router.include_router(api_router)

import os

from fastapi import FastAPI

from pxm_resources.api_resource import router as api_router

# FastAPI Router Definition
router = FastAPI(
    title='ProjectX Music API',
    version=os.getenv('pxm.version') or 'n/a'
)

# Attach API Router
router.include_router(api_router)

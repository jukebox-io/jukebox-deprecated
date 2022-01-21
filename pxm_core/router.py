from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pxm_commons.enums import Config
from pxm_core.docs import get_rapidoc_html
from pxm_resources.api_resource import router as api_router
from pxm_utils.config_utils import read_config

# FastAPI Router Definition
router = FastAPI(
    title='ProjectX Music API',
    version=read_config(Config.APP.VERSION) or 'n/a',
    docs_url=None, redoc_url=None  # Disable builtin docs
)

# Attach API Router
router.include_router(api_router)


# Attach api docs endpoint
@router.get('/api/docs', include_in_schema=False)
async def get_rapidoc() -> HTMLResponse:
    return get_rapidoc_html(
        openapi_url=router.openapi_url,
        title=f'{router.title} Docs'
    )

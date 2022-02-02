from fastapi import APIRouter, Depends, Path

from pxm_commons.enums import ApiVersionEnum
from pxm_resources.album_resource import router as album_router
from pxm_resources.artist_resource import router as artist_router
from pxm_resources.track_resource import router as track_router
from pxm_resources.user_resource import router as user_router
from pxm_security.security import verify_user_authorization


async def get_api_version(
        version: ApiVersionEnum = Path(..., example=ApiVersionEnum.V1, description="API Version Info"),
) -> ApiVersionEnum:
    """Gets the API version associated with the endpoint"""
    return version


# API Router Definition
router = APIRouter(
    prefix='/api/{version}',
    dependencies=[
        Depends(get_api_version),
        Depends(verify_user_authorization)
    ]
)

# Attach Artist API Router
router.include_router(artist_router)

# Attach Album API Router
router.include_router(album_router)

# Attach Track API Router
router.include_router(track_router)

# Attach User API Router
router.include_router(user_router)

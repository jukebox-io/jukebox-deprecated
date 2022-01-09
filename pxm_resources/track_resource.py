import fastapi

from pxm_models.models import Track

router = fastapi.APIRouter(prefix='/track', tags=['Track'])


@router.get('/', response_model=list[Track])
async def get_all_tracks():
    pass
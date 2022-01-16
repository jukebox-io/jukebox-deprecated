import fastapi

from pxm_models.models import TrackModel

router = fastapi.APIRouter(prefix='/track', tags=['Track'])


@router.get('/', response_model=list[TrackModel])
async def get_all_tracks():
    pass
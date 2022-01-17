import fastapi

from pxm_models.models import TrackSummary

router = fastapi.APIRouter(prefix='/track', tags=['Track'])


@router.get('/', response_model=list[TrackSummary])
async def get_all_tracks():
    pass

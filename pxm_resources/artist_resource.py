import fastapi

from pxm_models.models import ArtistSummary

router = fastapi.APIRouter(prefix='/artist', tags=['Artist'])


@router.get('/', response_model=list[ArtistSummary])
async def get_all_artists():
    pass

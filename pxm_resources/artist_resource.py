import fastapi

from pxm_models.models import ArtistModel

router = fastapi.APIRouter(prefix='/artist', tags=['Artist'])


@router.get('/', response_model=list[ArtistModel])
async def get_all_artists():
    pass

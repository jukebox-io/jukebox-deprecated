import fastapi

from pxm_models.models import Artist

router = fastapi.APIRouter(prefix='/artist', tags=['Artist'])


@router.get('/', response_model=list[Artist])
async def get_all_artists():
    pass

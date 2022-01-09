import fastapi

from pxm_models.models import Album

router = fastapi.APIRouter(prefix='/album', tags=['Album'])


@router.get('/', response_model=list[Album])
async def get_all_albums():
    pass
import fastapi

from pxm_models.models import AlbumModel

router = fastapi.APIRouter(prefix='/album', tags=['Album'])


@router.get('/', response_model=list[AlbumModel])
async def get_all_albums():
    pass
import fastapi

from pxm_models.models import AlbumSummary

router = fastapi.APIRouter(prefix='/album', tags=['Album'])


@router.get('/', response_model=list[AlbumSummary])
async def get_all_albums():
    pass

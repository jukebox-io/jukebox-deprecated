import fastapi

from pxm_commons.errors import PxmServiceError
from pxm_models.models import Album
from pxm_services import album_service

router = fastapi.APIRouter(prefix='/album', tags=['Album'])


@router.get('/', response_model=list[Album])
async def get_top_albums() -> list[Album]:
    try:
        top_albums: list[Album] = list()

        for album in album_service.get_top_albums():
            top_albums.append(
                Album(
                    id=album.pid,
                    name=album.title,
                )
            )
        return top_albums
    except PxmServiceError:
        # TODO: Log the error
        return []

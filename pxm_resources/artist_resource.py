import fastapi

from pxm_commons.errors import PxmServiceError
from pxm_models.models import Artist
from pxm_services import artist_service

router = fastapi.APIRouter(prefix='/artist', tags=['Artist'])


@router.get('/', response_model=list[Artist])
async def get_top_artists() -> list[Artist]:
    try:
        top_artists: list[Artist] = list()

        for artist in artist_service.get_top_artists():
            top_artists.append(
                Artist(
                    id=artist.pid,
                    name=artist.name,
                )
            )
        return top_artists
    except PxmServiceError:
        # TODO: Log the error
        return []

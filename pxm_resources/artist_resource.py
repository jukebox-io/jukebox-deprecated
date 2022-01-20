import fastapi

from pxm_commons.errors import PxmServiceError
from pxm_models.entities import ArtistEntity
from pxm_models.models import Artist
from pxm_services import artist_service

router = fastapi.APIRouter(prefix='/artist', tags=['Artist'])


@router.get('/', response_model=list[Artist])
async def get_top_artists() -> list[Artist]:
    try:
        top_artists: list[Artist] = list()

        for artist_entity in artist_service.get_top_artists():
            top_artists.append(
                convert_to_artist(artist_entity),
            )
        return top_artists
    except PxmServiceError:
        raise
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Top Artists list') from e


# // ---------------------------------------------------------------------------------------------- transformation fns

def convert_to_artist(artist_entity: ArtistEntity):
    return Artist(
        id=artist_entity.pid,
        name=artist_entity.name,
    )

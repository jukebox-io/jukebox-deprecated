import pxm_commons.entity_manager as em
from pxm_commons.errors import PxmServiceError
from pxm_models.entities import ArtistEntity


def get_artist_by_pid(pid: int) -> ArtistEntity:
    try:
        return em.create_query(ArtistEntity).get(pid)
    except PxmServiceError as e:
        raise e
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Artist by pid', e)

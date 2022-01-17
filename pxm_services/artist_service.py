import pxm_commons.entity_manager as em
from pxm_commons.errors import PxmServiceError
from pxm_models.entities import ArtistEntity


def get_top_artists() -> list[ArtistEntity]:
    """Get Top Artists List

    This function retrieves a list of most tending artists.
    """
    try:
        # TODO: Get from Network
        return []
    except PxmServiceError as e:
        raise e
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Top Artists list', e)


def get_artist_by_pid(pid: int) -> ArtistEntity:
    try:
        return em.create_query(ArtistEntity).get(pid)
    except PxmServiceError as e:
        raise e
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Artist by pid', e)

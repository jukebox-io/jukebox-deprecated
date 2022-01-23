from pxm_commons.errors import PxmServiceError
from pxm_models.entities import AlbumEntity


def get_top_albums() -> list[AlbumEntity]:
    """Get Top Albums List

    This function retrieves a list of most tending albums.
    """
    try:
        # TODO: Get from Network
        return []
    except PxmServiceError:
        raise
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Top Albums list') from e

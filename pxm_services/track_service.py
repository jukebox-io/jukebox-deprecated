from pxm_commons.errors import PxmServiceError
from pxm_models.entities import TrackEntity


def get_top_tracks() -> list[TrackEntity]:
    """Get Top Albums List

    This function retrieves a list of most tending albums.
    """
    try:
        # TODO: Get from Network
        return []
    except PxmServiceError as e:
        raise e
    except Exception as e:
        raise PxmServiceError('Failed to retrieve Top Tracks list', e)

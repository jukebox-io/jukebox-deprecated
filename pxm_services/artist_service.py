import pxm_commons.entity_manager as em
from pxm_models.entities import ArtistEntity


def get_artist_by_pid(pid: int) -> ArtistEntity:
    return em.create_query(ArtistEntity).get(pid)

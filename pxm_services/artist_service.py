import pylast
from sqlalchemy.orm import Query

import pxm_commons.entity_manager as em
from pxm_commons.errors import PxmServiceError
from pxm_models.entities import ArtistEntity
from pxm_services import lastfm_service


def get_artist_by_pid(pid: int) -> ArtistEntity:
    """Get Artist with the given ID

    Args:
        pid (str): ID of the artist

    Returns:
        Associated artist entity
    """
    artist_entity: ArtistEntity = em.fetch_one(
        Query(ArtistEntity).filter(ArtistEntity.pid == pid)
    )

    if not artist_entity:
        raise PxmServiceError('Failed to retrieve Artist by pid')

    return artist_entity


def get_top_artists() -> list[ArtistEntity]:
    """Get Top Artists List

    This function retrieves a list of most tending artists.
    """
    top_artists: list[ArtistEntity] = list()

    for lastfm_artist in lastfm_service.list_trending_artists():
        top_artists.append(
            _create_new_artist_from_lastfm_if_not_exists(lastfm_artist),
        )

    return top_artists


def _create_new_artist_from_lastfm_if_not_exists(lastfm_artist: pylast.Artist,
                                                 in_transaction: bool = False) -> ArtistEntity:
    artist_name: str = lastfm_artist.get_name(properly_capitalized=True)
    artist_entity: ArtistEntity = em.fetch_one(
        Query(ArtistEntity).filter(ArtistEntity.name == artist_name)
    )

    if artist_entity:
        return artist_entity

    try:
        if not in_transaction:
            em.begin_transaction()

        # Add lastfm_artist
        artist_entity = ArtistEntity(
            name=artist_name,
        )

        if not in_transaction:
            em.get_transaction().commit()
        return artist_entity
    except:
        if not in_transaction:
            em.get_transaction().rollback()
        raise
    finally:
        if not in_transaction:
            em.end_transaction()

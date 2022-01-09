import pylast

import pxm_commons.entity_manager as em
from pxm_models.entities import ArtistEntity


def convert_to_entity_artist(pylast_artist: pylast.Artist) -> ArtistEntity:
    artist_name = pylast_artist.get_name(properly_capitalized=True)
    artist = em.create_query(ArtistEntity).where(ArtistEntity.name == artist_name).one_or_none()

    return artist

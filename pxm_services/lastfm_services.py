import os
import typing

import pylast

from pxm_services.service_exceptions import ServiceError, ValueError


def _get_env_or_raise_error(env_key: str, error_msg: str = None) -> str:
    env_value: str = os.getenv(env_key)
    if not env_value:
        raise ValueError(error_msg or f"Environment Variable '{env_key}' not found.")
    return env_value


_network = pylast.LastFMNetwork(
    api_key=_get_env_or_raise_error('LASTFM_API_KEY'),
    api_secret=_get_env_or_raise_error('LASTFM_API_SECRET'),
)  # Read only lastfm network instance

# Enable cache handling mechanism to avoid duplicate calls to the API endpoint.
_network.enable_caching()

# Enable rate limiting to ensure uninterrupted services without hitting the max request limit.
_network.enable_rate_limit()


# // -------------------------------------------------------------------------------------------- trending

def _extract_top_item(top_item: pylast.TopItem):
    return top_item.item


def list_trending_artists(limit: int = None, country: str = None) -> list[pylast.Artist]:
    """Get a list of the most played artists

    Args:
        limit (int): Maximum Number of items to be returned
        country (str): Optionally specify the country name

    Returns:
        List of most played artists in decreasing order
    """
    try:
        top_artist_list: list[pylast.TopItem]
        if country:
            top_artist_list = _network.get_geo_top_artists(limit=limit, country=country)
        else:
            top_artist_list = _network.get_top_artists(limit=limit)
        return list(map(_extract_top_item, top_artist_list))
    except pylast.PyLastError as e:
        raise ServiceError('Failed to retrieve trending Artist list from last.fm', e)


def list_trending_tracks(limit: int = None, country: str = None, location: str = None) -> list[pylast.Track]:
    """Get a list of the most played tracks

    Args:
        limit (int): Maximum Number of items to be returned
        country (str): Optionally specify the country name
        location (str): Optionally specify a location name within the country

    Returns:
        List of most played tracks in decreasing order
    """
    try:
        top_track_list: list[pylast.TopItem]
        if country:
            top_track_list = _network.get_geo_top_tracks(limit=limit, country=country, location=location)
        else:
            top_track_list = _network.get_top_tracks(limit=limit)
        return list(map(_extract_top_item, top_track_list))
    except pylast.PyLastError as e:
        raise ServiceError('Failed to retrieve trending Track list from last.fm', e)


# // --------------------------------------------------------------------------------------------- find by id

def find_album_by_id(id: str) -> typing.Optional[pylast.Album]:
    """Finds an Album by its MusicBrainz ID

    Args:
        id (str): ID of the Album to be found.

    Returns:
        Returns the Album associated with the given ID. If the Album is not found it returns None
    """
    try:
        return _network.get_album_by_mbid(mbid=id)
    except pylast.PyLastError as e:
        return None


def find_artist_by_id(id: str) -> typing.Optional[pylast.Artist]:
    """Finds an Artist by its MusicBrainz ID

    Args:
        id (str): ID of the Artist to be found.

    Returns:
        Returns the Artist associated with the given ID. If the Artist is not found it returns None
    """
    try:
        return _network.get_artist_by_mbid(mbid=id)
    except pylast.PyLastError as e:
        return None


def find_track_by_id(id: str) -> typing.Optional[pylast.Track]:
    """Finds a Track by its MusicBrainz ID

    Args:
        id (str): ID of the Track to be found.

    Returns:
        Returns the Track associated with the given ID. If the Track is not found it returns None
    """
    try:
        return _network.get_track_by_mbid(mbid=id)
    except pylast.PyLastError as e:
        return None


# // ---------------------------------------------------------------------------------------------- search

def search_albums(album_name: str, page: int = 1) -> list[pylast.Album]:
    """Search for Album

    Args:
        album_name (str): Album Name
        page (int): Page Number to extract [default: 1]

    Returns:
        Paginated search results list
    """
    try:
        search_obj: pylast.AlbumSearch = _network.search_for_album(album_name=album_name)

        # HACK: This is an optimization hack and can be replaced by using loops
        search_obj._last_page_index = page - 1

        return search_obj.get_next_page()
    except pylast.PyLastError as e:
        raise ServiceError('Failed to retrieve Album Search Results from last.fm', e)


def search_artists(artist_name: str, page: int = 1) -> list[pylast.Artist]:
    """Search for Artist

    Args:
        artist_name (str): Artist Name
        page (int): Page Number to extract [default: 1]

    Returns:
        Paginated search results list
    """
    try:
        search_obj: pylast.ArtistSearch = _network.search_for_artist(artist_name=artist_name)

        # HACK: This is an optimization hack and can be replaced by using loops
        search_obj._last_page_index = page - 1

        return search_obj.get_next_page()
    except pylast.PyLastError as e:
        raise ServiceError('Failed to retrieve Artist Search Results from last.fm', e)


def search_track(track_name: str, artist_name: str = None, page: int = 1) -> list[pylast.Track]:
    """Search for Track

    Args:
        track_name (str): Track Name
        artist_name (str): Artist Name
        page (int): Page Number to extract [default: 1]

    Returns:
        Paginated search results list
    """
    try:
        search_obj: pylast.TrackSearch = _network.search_for_track(track_name=track_name, artist_name=artist_name or '')

        # HACK: This is an optimization hack and can be replaced by using loops
        search_obj._last_page_index = page - 1

        return search_obj.get_next_page()
    except pylast.PyLastError as e:
        raise ServiceError('Failed to retrieve Track Search Results from last.fm', e)

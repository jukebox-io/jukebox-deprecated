import typing as ty

import pydantic as pyd


class BaseModel(pyd.BaseModel):
    pass


# // --------------------------------------------------------------------------------------- entity models

class _CommonNameIdFields(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this',
    )


# Artist Entity

class Artist(_CommonNameIdFields):
    pass


class ArtistSummary(Artist):
    pass


# Album Entity

class Album(_CommonNameIdFields):
    pass


class AlbumSummary(Album):
    artist: Artist = pyd.Field(
        None,
        description='Associated Artist Entity',
    )


# Track Entity

class Track(_CommonNameIdFields):
    pass


class TrackSummary(Track):
    artist: Artist = pyd.Field(
        None,
        description='Associated Artist Entity',
    )
    album: ty.Optional[Album] = pyd.Field(
        None,
        description='Associated Album Entity, or null if the track is a single',
    )


# // --------------------------------------------------------------------------------------- user models

class User(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this user',
    )
    email: pyd.EmailStr = pyd.Field(
        None,
        description='Email address for this user',
    )

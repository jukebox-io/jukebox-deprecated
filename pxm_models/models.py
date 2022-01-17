import typing as ty

import pydantic as pyd


class BaseModel(pyd.BaseModel):
    pass


# // --------------------------------------------------------------------------------------- entity models

# Artist Entity

class Artist(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this artist',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this artist',
    )


class ArtistSummary(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this artist',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this artist',
    )


# Album Entity

class Album(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this album',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this album',
    )


class AlbumSummary(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this album',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this album',
    )
    artist: Artist = pyd.Field(
        None,
        description='Associated Artist Entity',
    )


# Track Entity

class Track(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this track',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this track',
    )


class TrackSummary(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this track',
    )
    name: str = pyd.Field(
        None,
        description='A human readable name for this track',
    )
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

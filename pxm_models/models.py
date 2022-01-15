import typing as ty

import pydantic


class _BaseModel(pydantic.BaseModel):
    pass


class Artist(_BaseModel):
    id: int
    name: str


class Album(_BaseModel):
    id: int
    title: str
    artist: Artist


class Track(_BaseModel):
    id: int
    title: str
    artist: Artist
    album: ty.Optional[Album]

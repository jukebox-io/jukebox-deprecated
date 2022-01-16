import typing as ty

import pydantic


class _BaseModel(pydantic.BaseModel):
    pass


# // --------------------------------------------------------------------------------------- consolidated models

class _BaseNameAndPidModel(_BaseModel):
    pid: int
    name: str


class ArtistNameAndPidModel(_BaseNameAndPidModel):
    pass


class AlbumNameAndPidModel(_BaseNameAndPidModel):
    pass


class TrackNameAndPidModel(_BaseNameAndPidModel):
    pass


# // --------------------------------------------------------------------------------------- entity models

class ArtistModel(_BaseModel):
    pid: int
    name: str


class AlbumModel(_BaseModel):
    pid: int
    name: str
    artist: ArtistNameAndPidModel


class TrackModel(_BaseModel):
    pid: int
    name: str
    artist: ArtistNameAndPidModel
    album: ty.Optional[AlbumNameAndPidModel]

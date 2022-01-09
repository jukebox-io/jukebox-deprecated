import pydantic


class Model(pydantic.BaseModel):
    pass


class Artist(Model):
    id: int
    name: str


class Album(Model):
    id: int
    title: str
    artist: Artist


class Track(Model):
    id: int
    title: str
    artist: Artist
    album: Album

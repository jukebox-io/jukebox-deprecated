from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class BaseEntity(declarative_base()):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}


class ArtistEntity(BaseEntity):
    __tablename__ = 'artist'

    # Columns
    pid: int = Column('pid', Integer, primary_key=True)
    name: str = Column('name', String)

    # Methods
    def __init__(self, name: str):
        self.name = name


class AlbumEntity(BaseEntity):
    __tablename__ = 'artist'

    # Columns
    pid: int = Column('pid', Integer, primary_key=True)
    title: str = Column('title', String)
    artist_pid: int = Column('artist_pid', Integer, ForeignKey(ArtistEntity.pid))

    # Methods
    def __init__(self, title: str, artist_pid: int):
        self.title = title
        self.artist_pid = artist_pid


class TrackEntity(BaseEntity):
    __tablename__ = 'track'

    # Columns
    pid: int = Column('pid', Integer, primary_key=True)
    title: str = Column('title', String)
    artist_pid: int = Column('artist_pid', Integer, ForeignKey(ArtistEntity.pid))
    album_pid: int = Column('album_pid', Integer, ForeignKey(AlbumEntity.pid))

    # Methods
    def __init__(self, title: str, artist_pid: int, album_pid: int):
        self.title = title
        self.artist_pid = artist_pid
        self.album_pid = album_pid

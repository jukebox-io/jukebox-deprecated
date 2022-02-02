from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class BaseEntity(declarative_base()):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'extend_existing': True
    }


class ArtistEntity(BaseEntity):
    __tablename__ = 'artist'

    # Columns
    pid: int = Column('pid', Integer, primary_key=True)
    name: str = Column('name', String)

    # Methods
    def __init__(self, name: str):
        self.name = name


class AlbumEntity(BaseEntity):
    __tablename__ = 'album'

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
    album_pid: int | None = Column('album_pid', Integer, ForeignKey(AlbumEntity.pid))

    # Methods
    def __init__(self, title: str, artist_pid: int, album_pid: int = None):
        self.title = title
        self.artist_pid = artist_pid
        self.album_pid = album_pid


class UserEntity(BaseEntity):
    __tablename__ = 'user'

    # Columns
    pid: int = Column('pid', Integer, primary_key=True)
    user_name: str = Column('user_name', String)
    email: str | None = Column('email', String)
    phone_no: str | None = Column('phone_no', String)
    hashed_password: str = Column('hashed_password', String)

    # Methods
    def __init__(self, user_name: str, hashed_password: str, email: str = None, phone_no: str = None):
        self.user_name = user_name
        self.email = email
        self.phone_no = phone_no
        self.hashed_password = hashed_password

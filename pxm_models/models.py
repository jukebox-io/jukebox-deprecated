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


# // --------------------------------------------------------------------------------------- security models

class User(BaseModel):
    id: int = pyd.Field(
        None,
        description='Unique identifier for this user',
    )
    uname: str = pyd.Field(
        description='Unique User Name for this user',
    )


class UserSummary(User):
    email: pyd.EmailStr | None = pyd.Field(
        default=None,
        description='Unique Email address for this user',
    )
    ph_no: str | None = pyd.Field(
        default=None,
        description="Unique Email address for this user",
        regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    )


class UserLoginInput(BaseModel):
    uid: str = pyd.Field(
        description='User Name, Email or Phone Number for this user'
    )
    password: str = pyd.Field(
        description='Password for this user',
        min_length=10,
    )


class AccessToken(BaseModel):
    access_token: str = pyd.Field(
        description='Access Token for this User',
    )
    token_type: str = pyd.Field(
        description='Token Type for this Token',
    )

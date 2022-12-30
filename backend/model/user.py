from pydantic import EmailStr, constr

from .base import BaseModel, IDModelMixin, DateTimeModelMixin


class UserBase(BaseModel):
    email: EmailStr
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: constr(min_length=7, max_length=100)


class UserInDB(UserBase, IDModelMixin, DateTimeModelMixin):
    password: constr(min_length=7, max_length=100)
    salt: str


class User(UserBase, IDModelMixin, DateTimeModelMixin):
    pass

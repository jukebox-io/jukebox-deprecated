from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from pxm_models.entities import UserEntity
from pxm_models.models import User, UserLoginInput, AccessToken
from pxm_services import user_service

_auth_scheme = OAuth2PasswordBearer(
    tokenUrl='api/o/oauth2/token',
    description='Oauth 2.0 password authentication',
    scopes={
        'scrobbler': 'Edit, configure, and delete your data'
    }
)


def perform_login(user_input: UserLoginInput) -> AccessToken:
    """Perform login operation with the given Credentials"""
    return _create_access_token(
        user=_authenticate_user(user_input),
    )


def validate_authorization(to_decode: str = Depends(_auth_scheme)) -> None:
    """Validate Authentication Credentials

    Args:
        to_decode (str): Token to validate upon

    Returns:
        Throws auth errors on invalid tokens
    """
    try:
        decoded_jwt: dict = jwt.decode(to_decode, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = decoded_jwt['sub']

        # Check User
        user_entity: UserEntity = user_service.get_user_by_pid(user_id)
        _check_user_entity(user_entity)

    except AuthError:
        raise
    except Exception as e:
        raise AuthError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
        ) from e


class AuthError(HTTPException):
    def __init__(self, status_code: int, detail):
        super().__init__(status_code, detail, headers={'WWW-Authenticate': 'Bearer'})


# // --------------------------------------------------------------------------------------------- Token Builder

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Demo only
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _create_access_token(user: User) -> AccessToken:
    to_encode = {
        "sub": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return AccessToken(
        access_token=encoded_jwt,
        token_type='bearer'
    )


# // --------------------------------------------------------------------------------------------- Password Validator

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    # TODO: Replace 'hashed_password' with user.hashed_password
    return _pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str) -> str:
    """Build hash of given password"""
    return _pwd_context.hash(password)


def _authenticate_user(user_input: UserLoginInput) -> User:
    """Get Authenticated User"""
    user_entity: UserEntity = user_service.get_user_by_uid(user_input.uid)

    # verify password
    if _verify_password(user_input.password, user_entity.hashed_password):
        raise AuthError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect Password',
        )

    # Check User
    _check_user_entity(user_entity)

    return User(
        id=user_entity.pid,
        user_name=user_entity.user_name,
    )


def _check_user_entity(user_entity: UserEntity) -> None:
    pass

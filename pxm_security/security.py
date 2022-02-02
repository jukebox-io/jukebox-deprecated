from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from pxm_models.entities import UserEntity
from pxm_models.models import User, UserLoginInput, AccessToken
from pxm_services import user_service

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Demo only
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_oauth_scheme = OAuth2PasswordBearer(
    tokenUrl='api/o/oauth2/token',
    description='Oauth 2.0 password authentication'
)
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# // --------------------------------------------------------------------------------------------- API

def login_user(user_login_creds: UserLoginInput) -> AccessToken:
    """Perform login operation with the given Credentials"""
    try:
        user: User = _authenticate_user_login(user_login_creds)
        return _build_access_token(user)
    except AuthError:
        raise
    except Exception as e:
        raise AuthError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not validate credentials',
        ) from e


def register_new_user(user) -> AccessToken:
    """Perform signup operation with the given Credentials"""
    pass


def verify_user_authorization(token: str = Depends(_oauth_scheme)) -> None:
    """Validate Authentication Credentials

    Args:
        token (str): Token to validate upon

    Returns:
        Throws auth errors on invalid tokens
    """
    try:
        decoded_jwt: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = decoded_jwt['sub']

        # Verify User Access Permission
        user_entity: UserEntity = user_service.get_user_by_pid(user_id)
        _verify_user_access(user_entity)

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

def _build_access_token(user: User) -> AccessToken:
    """Builds an access token for the given user"""
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

def _verify_password(user: UserEntity, password: str) -> bool:
    """Verifies that the user with the given password"""
    return _pwd_context.verify(password, user.hashed_password)


def _build_hash(password: str) -> str:
    """Build hash of given password"""
    return _pwd_context.hash(password)


def _authenticate_user_login(user_input: UserLoginInput) -> User:
    """Get Authenticated User"""
    user_entity: UserEntity = user_service.get_user_by_uid(user_input.uid)

    # verify password
    if _verify_password(user_entity, user_input.password):
        raise AuthError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect Password',
        )

    # Verify User Access Permission
    _verify_user_access(user_entity)

    return User(
        id=user_entity.pid,
        user_name=user_entity.user_name,
    )


def _verify_user_access(user_entity: UserEntity) -> None:
    # Everyone is allowed to access for now
    pass

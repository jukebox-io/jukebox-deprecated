#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.
#
#  This file is part of the JukeBox Music App and and is released under the "MIT License Agreement".
#  Please see the LICENSE file that should have been included as part of this package.

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError  # noqa
from passlib.context import CryptContext
from starlette.datastructures import Secret
from starlette.status import HTTP_403_FORBIDDEN

from jukebox.settings import settings

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

ALGORITHM: str = "HS256"

JWT_SECRET_KEY: Secret = settings.get('JWT_SECRET_KEY', cast=Secret)  # should be kept secret
JWT_REFRESH_SECRET_KEY: Secret = settings.get('JWT_REFRESH_SECRET_KEY', cast=Secret)  # should be kept secret

# Security Context
bearer_auth = HTTPBearer(
    bearerFormat='JWT',
    scheme_name='bearerAuth',
    description="JWT Bearer authentication scheme. Clients must include a JWT token in the 'Authorization' header of "
                "each request with the format 'Bearer &lt;token&gt;'.",
    auto_error=True,
)


def check_access(request: Request, credentials=Depends(bearer_auth)) -> None:
    """FastAPI dependency to check and validate access to API endpoints"""
    auth_token: str = credentials.credentials

    # Decode JWT token
    try:
        claims: dict = jwt.decode(auth_token, str(JWT_SECRET_KEY), algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token"
        )

    # Save for future use
    request.state["auth"] = auth_token
    request.state["user"] = claims["sub"]


# Password Access

# Create a new CryptContext with bcrypt as the default algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(secret: str) -> str:
    """Generates a new password hash"""
    return pwd_context.hash(secret)


def validate_password(secret: str, hashed_secret: str) -> bool:
    """Validates the password hash"""
    return pwd_context.verify(secret, hashed_secret)

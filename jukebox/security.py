from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

from jukebox.settings import JWT_SECRET, JWT_ALGORITHM

BEARER_FORMAT: str = "JWT"
SCHEMA_NAME: str = "bearerAuth"
DESCRIPTION: str = "JWT Bearer authentication scheme. Clients must include a JWT token in the 'Authorization' header " \
                   "of each request with the format 'Bearer &lt;token&gt;'."

# Security Context
bearer_auth = HTTPBearer(bearerFormat=BEARER_FORMAT, scheme_name=SCHEMA_NAME, description=DESCRIPTION, auto_error=True)


def has_access(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer_auth)) -> None:
    """FastAPI dependency to check and validate access to API endpoints"""
    auth_token: str = credentials.credentials

    # Decode JWT token
    try:
        claims: dict = jwt.decode(auth_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
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


def validate_password(secret: str, hash: str) -> bool:
    """Validates the password hash"""
    return pwd_context.verify(secret, hash)

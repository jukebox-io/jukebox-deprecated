from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=True)

    async def __call__(self, request: Request) -> None:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        token: str = credentials.credentials

        # Decode JWT token
        try:
            claims: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )

        # Verify
        user_id: str = claims["sub"]

        # Save for future use
        request.state["auth"] = token
        request.state["user"] = user_id


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
security_context = JWTBearer()

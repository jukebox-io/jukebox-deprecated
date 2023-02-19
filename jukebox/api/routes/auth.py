from fastapi import APIRouter
from jose import jwt
from jukebox.services.security import SECRET_KEY, ALGORITHM

router = APIRouter()


@router.post('/token')
async def login():
    access_token = jwt.encode({"sub": "user1"}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

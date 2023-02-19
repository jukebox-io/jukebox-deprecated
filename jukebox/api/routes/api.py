from fastapi import APIRouter, Depends
from jukebox.services.security import security_context
from jukebox.api.routes import auth

# Authenticated Routes
protected_router = APIRouter(
    dependencies=[Depends(security_context)]
)


@protected_router.get('/private')
async def private():
    return


# Base routes
router = APIRouter(prefix='/api')
router.include_router(protected_router)
router.include_router(auth.router, prefix='/auth')


@router.get('/healthcheck')
async def healthcheck():
    return {"status": "ok"}

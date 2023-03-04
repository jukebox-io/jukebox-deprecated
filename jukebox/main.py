from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from jukebox.security import has_access
from jukebox.settings import ALLOWED_HOSTS, CORS_MAX_AGE, API_PREFIX

# Let's create the Web API framework
app = FastAPI(title='JukeBox API')

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=CORS_MAX_AGE,
)

# Authenticated Routes
private_router = APIRouter()

# Un-Authenticated Routes
public_router = APIRouter()


@public_router.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}


@private_router.get("/private")
async def private() -> dict:
    return {"status": "ok"}


# Include API routers
app.include_router(
    private_router, prefix=API_PREFIX,
    dependencies=[Depends(has_access)],
    responses={
        401: {"description": "Invalid or expired token"},  # HTTP_401_UNAUTHORIZED
        403: {"description": "User does not have permission to access this resource"}  # HTTP_403_FORBIDDEN
    },
)
app.include_router(public_router, prefix=API_PREFIX)

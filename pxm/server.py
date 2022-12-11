from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pxm.settings import ALLOWED_HOSTS, APP_VERSION

# Initialize FastAPI Application
router = FastAPI(
    title='ProjectX Music API',
    version=APP_VERSION,
    description=f'A Music Recommendation System made using Flutter and backed by FastAPI.',
    license_info={
        "name": "MIT",
        "url": "https://github.com/ProjectX-Music/ProjectX-Music/blob/develop/LICENSE",
    },
    redoc_url='/'
)

# Configure Additional Routers


# Configure CORS Headers (Cross-Origin Resource Sharing)
router.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

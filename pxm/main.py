from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import CommaSeparatedStrings

from pxm.core.settings import config
from pxm.version import pxm_version

# Initialize FastAPI Application
app = FastAPI(
    title='ProjectX Music API',
    version=pxm_version,
    description=f'A Music Recommendation System made using Flutter and backed by FastAPI.',
    license_info={
        "name": "MIT",
        "url": "https://github.com/ProjectX-Music/ProjectX-Music/blob/develop/LICENSE",
    },
)

# Configure Additional Routers


# Configure CORS Headers (Cross-Origin Resource Sharing)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default='*')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .version import __version__ as app_version

# Initialize FastAPI Application
app = FastAPI(
    title='ProjectX Music API',
    version=app_version
)

# Configure Additional Routers


# Configure CORS Headers (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

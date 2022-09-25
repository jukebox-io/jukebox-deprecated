from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.version import read_version_info

__all__ = ['app']

# Initialize FastAPI Application
app = FastAPI(title='ProjectX Music API', version=read_version_info())

# Configure Additional Routers

# Configure CORS (Cross-Origin Resource Sharing)
origins = [
    'http://localhost',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Configure Endpoints

@app.get('/')
async def root():
    return {'status': 'up'}

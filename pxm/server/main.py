from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pxm.server.api.routes import router as api_router
from pxm.server.version import version

__all__ = ['app']

# Initialize App
app = FastAPI(title='ProjectX Music API', version=version)

# Routers
app.include_router(api_router)

# CORS (Cross-Origin Resource Sharing)
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


# Endpoints

@app.get('/')
async def root():
    return {'status': 'up'}

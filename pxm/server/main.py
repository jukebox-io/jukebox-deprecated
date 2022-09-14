from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pxm.server.api.routes import router as api_router

app = FastAPI(title='ProjectX Music API', version='n/a')

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


@app.get('/')
async def root():
    return {'status': 'up'}

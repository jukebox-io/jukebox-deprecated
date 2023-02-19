from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from jukebox.core.settings import ALLOWED_HOSTS
from jukebox.api.routes import api

# Let's create the Web API framework
app = FastAPI(title='JukeBox API')

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=24 * 60 * 60,  # 1-day
)

# Include API router
app.include_router(api.router)

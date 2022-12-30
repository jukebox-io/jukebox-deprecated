from fastapi import FastAPI

from .model.user import User, UserCreate

# let's create the Web API framework
app = FastAPI(
    title="JukeBox API",
    version="latest",
    description="A Music Recommendation System made using Flutter and backed by FastAPI.",
    # docs_url=None,
    redoc_url="/"
)


@app.get('/api/user', response_model=User)
async def get_user() -> User:
    pass


@app.post('/api/user')
async def create_user(user: UserCreate):
    return {'id': user.email}

import fastapi

from pxm_models.entities import UserEntity
from pxm_models.models import User

router = fastapi.APIRouter(prefix='/users', tags=['User'])


@router.get('/me', response_model=User)
async def get_current_user() -> User:
    pass


# // ---------------------------------------------------------------------------------------------- transformation fns

def convert_to_user(user_entity: UserEntity) -> User:
    return User(
        id=user_entity.pid,
        user_name=user_entity.user_name,
    )

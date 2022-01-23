from sqlalchemy.orm import Query

import pxm_commons.entity_manager as em
from pxm_commons.errors import PxmServiceError
from pxm_models.entities import UserEntity


def get_user_by_pid(pid: int) -> UserEntity:
    """Get User with the given ID

    Args:
        pid (str): ID of the user

    Returns:
        Associated user entity
    """
    user_entity: UserEntity = em.fetch_one(
        Query(UserEntity).filter(UserEntity.pid == pid)
    )

    if not user_entity:
        raise PxmServiceError('Failed to retrieve User by pid')

    return user_entity

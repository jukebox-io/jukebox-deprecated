from sqlalchemy.orm import Query

import pxm_commons.entity_manager as em
from pxm_commons.errors import PxmServiceError
from pxm_models.entities import UserEntity


def get_user_by_pid(pid: int) -> UserEntity:
    """Get User with the given ID

    Args:
        pid (int): ID of the user

    Returns:
        Associated user entity
    """
    user_entity: UserEntity = em.fetch_one(
        Query(UserEntity).filter(UserEntity.pid == pid)
    )

    if not user_entity:
        raise PxmServiceError('Failed to retrieve User by pid')

    return user_entity


def get_user_by_uid(uid: str) -> UserEntity:
    """Get User with the given ID

    Args:
        uid (str): Username, Email or Phone Number of the user

    Returns:
        Associated user entity
    """
    user_entity: UserEntity = em.fetch_one(
        Query(UserEntity).filter((UserEntity.user_name == uid) | (UserEntity.email == uid) | (UserEntity.phone_no == uid))
    )

    if not user_entity:
        raise PxmServiceError('Failed to retrieve User by its uid')

    return user_entity

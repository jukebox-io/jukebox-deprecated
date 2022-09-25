from sqlalchemy import orm

__all__ = ['BaseEntity', 'BaseTopEntity']


# Base Entity
class BaseEntity(orm.declarative_base()):
    pass


# Base Top Entity
class BaseTopEntity(BaseEntity):
    pass

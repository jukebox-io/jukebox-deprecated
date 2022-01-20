import os
import typing

import sqlalchemy.orm

from pxm_models.entities import BaseEntity

_engine = sqlalchemy.create_engine(os.environ['database.url'], future=True)

# Shared session instance
_session = sqlalchemy.orm.Session(bind=_engine, future=True)


# // --------------------------------------------------------------------------------------------- query api

def fetch_all(query: sqlalchemy.orm.Query) -> list[BaseEntity]:
    return query.with_session(_session).all()


def fetch_one(query: sqlalchemy.orm.Query) -> BaseEntity:
    return query.with_session(_session).one_or_none()


# // --------------------------------------------------------------------------------------------- transactions api

def begin_transaction() -> None:
    """Begin a transaction, or raise error if one already begun"""
    _session.begin()


def end_transaction() -> None:
    """Close any existing transaction"""
    if in_transaction():
        _session.close()


def in_transaction() -> bool:
    """Has a transaction has already begun?"""
    return _session.in_transaction()


def get_transaction() -> typing.Optional[sqlalchemy.orm.SessionTransaction]:
    """Get the current transaction instance if a transaction has already begun, else None"""
    return _session.get_transaction()

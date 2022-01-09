import os
import typing

import sqlalchemy.orm

_engine = sqlalchemy.create_engine(os.environ['database.url'], future=True)

# Shared session instance
_session = sqlalchemy.orm.Session(bind=_engine, future=True)


# // --------------------------------------------------------------------------------------------- query builder

def create_query(*entities, **kwargs) -> sqlalchemy.orm.Query:
    """Build a new Sqlalchemy Query

    e.g.,

    create_query

    Args:
        entities: a sequence of entities and/or SQL expressions.

    Returns:
        A new Query instance.
    """
    return _session.query(*entities, **kwargs)


def execute(stmt) -> sqlalchemy.engine.Result:
    return _session.execute(stmt)


# // --------------------------------------------------------------------------------------------- transactions api

def begin_transaction() -> None:
    """Begin a transaction, or raise error if one already begun"""
    _session.begin()


def end_transaction() -> None:
    """Close any existing transaction"""
    if in_transaction():
        get_transaction().close()


def in_transaction() -> bool:
    """Has a transaction has already begun?"""
    return _session.in_transaction()


def get_transaction() -> typing.Optional[sqlalchemy.orm.SessionTransaction]:
    """Get the current transaction instance if a transaction has already begun, else None"""
    return _session.get_transaction()

import os

from sqlalchemy import create_engine, orm

__all__ = ['SessionFactory']

DATABASE_URL = os.environ.get('DATABASE_URL') or r'sqlite://'

# Create new connection
engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}, echo=True, future=True
)

# Create new session factory
SessionFactory = orm.sessionmaker(bind=engine)

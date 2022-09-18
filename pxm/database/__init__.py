import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ['SessionLocal', 'Base']

DATABASE_URL = os.environ.get('DATABASE_URL') or r'sqlite://'

# Create new connection
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine)

# Schema Base
Base = declarative_base()

from sqlalchemy import orm
from app.database.session import SessionFactory


# Create new database session
def create_db_session() -> orm.Session:
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.engine.url import URL

from falconer.db.model import Base


def get_url() -> URL:
    """Get database connection URL.

    Connection URL parts are extracted from environment variables.

    """
    return URL(
        drivername=os.getenv('DB_DRIVER_NAME', None),
        username=os.getenv('DB_USERNAME', None),
        password=os.getenv('DB_PASSWORD', None),
        host=os.getenv('DB_HOST', None),
        port=os.getenv('DB_PORT', None),
        database=os.getenv('DB_NAME', None),
        query=os.getenv('DB_QUERY', None)
    )


def get_session_factory():
    engine = create_engine(get_url())
    Base.metadata.bind = engine
    return orm.sessionmaker(bind=engine)


def get_scoped_session_factory():
    return orm.scoped_session(get_session_factory())


@contextmanager
def session_scope() -> Generator[orm.Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session_factory = get_session_factory()
    session = session_factory()  # type: orm.Session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

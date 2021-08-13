from typing import Generator

from _pytest.fixtures import fixture
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from library_api.db.session import Base

test_engine: Engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
test_session: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db_session() -> Generator:
    try:
        session = test_session()
        yield session
    finally:
        session.close()


@fixture(autouse=True)
def run_around_each_test() -> Generator:
    # before test
    Base.metadata.create_all(bind=test_engine)
    # run test
    yield
    # after test
    Base.metadata.drop_all(bind=test_engine)

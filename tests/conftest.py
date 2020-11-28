import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture()
def session():
    from src.database import engine, metadata, session

    metadata.create_all(bind=engine)

    yield session

    session.close()
    metadata.drop_all(bind=engine)

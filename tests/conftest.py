import pytest


@pytest.fixture()
def session():
    from src.database import Model, db

    with db("sqlite://", echo=False) as db:
        engine = db.engine
        session = db.session

        Model.metadata.create_all(bind=engine)

        yield session

    session.close()
    Model.metadata.drop_all(bind=engine)

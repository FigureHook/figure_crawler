import pytest


@pytest.fixture()
def session():
    from src.database import Model, db, metadata

    with db("sqlite://", echo=False) as db:
        engine = db.engine
        session = db.session

        metadata.create_all(bind=engine)
        Model.set_session(session)
        yield session

    Model.set_session(None)
    session.close()
    metadata.drop_all(bind=engine)

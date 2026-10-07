import os
import importlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Never initialize the local development database while testing.
os.environ["DATABASE_URL"] = "sqlite://"


@pytest.fixture
def client():
    module = importlib.import_module("app.main")
    from app.db import Base, get_db

    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)

    def override_db():
        with sessions() as session:
            yield session

    module.app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(module.app) as test_client:
            test_client.sessions = sessions
            yield test_client
    finally:
        module.app.dependency_overrides.clear()
        engine.dispose()

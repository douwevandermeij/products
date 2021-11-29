import pytest


@pytest.fixture
def client():
    from starlette.testclient import TestClient

    from app.main import app

    return TestClient(app)

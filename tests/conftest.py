import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import get_storage


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    get_storage().reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

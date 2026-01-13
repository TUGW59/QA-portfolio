import pytest
from fastapi.testclient import TestClient
from app.main import app, _USERS

@pytest.fixture(autouse=True)
def clear_users():
    # Each test starts with clean in-memory DB
    _USERS.clear()
    yield
    _USERS.clear()

@pytest.fixture()
def client():
    return TestClient(app)

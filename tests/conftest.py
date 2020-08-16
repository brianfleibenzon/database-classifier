import pytest
from app import create_app
from app.helpers.database import initDB

@pytest.fixture()
def app():
    app = create_app({"MONGO_URI": "mongodb://localhost:27017/classifierTests", "CRYPTO_KEY": "KYCbSsOCWCOSZ_J1St6se_HW8ne0mOOJFgOutSsnCxo=", "JWT_KEY": "test"})
    
    # create the database and load test data
    with app.app_context():
        initDB()

    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="admin", password="teSt@123"):
        return self._client.post(
            "/api/v1/auth/login", data={"username": username, "password": password}
        )

    def header(self):
        return {'Authorization': 'Bearer {}'.format(self.login().get_json().get("token"))}

@pytest.fixture
def auth(client):
    return AuthActions(client)
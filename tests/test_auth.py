import pytest

def test_register(client):
    response = client.post("/api/v1/auth/register", data={"username": "test", "password": "test111"})
    assert response.status_code == 201

@pytest.mark.parametrize(
    ("username", "password", "message", "status"),
    (
        ("", "", "Parameter 'username' was not provided or is invalid", 400),
        ("test", "", "Parameter 'password' was not provided or is invalid", 400),
        ("admin", "test", "The username is already registered", 409)
    )
)
def test_register_validate_input(client, username, password, message, status):
    response = client.post("/api/v1/auth/register", data={"username": username, "password": password})
    assert message == response.get_json().get("msg")
    assert status == response.status_code

def test_login(client, auth):
    response = auth.login()
    assert response.status_code == 200

@pytest.mark.parametrize(
    ("username", "password", "message", "status"),
    (
        ("", "", "Authentication credentials are not valid", 402),
        ("admin", "", "Authentication credentials are not valid", 402),
        ("admin", "test", "Authentication credentials are not valid", 402)
    )
)
def test_login_validate_input(auth, username, password, message, status):
    response = auth.login(username, password)
    assert message == response.get_json().get("msg")
    assert status == response.status_code

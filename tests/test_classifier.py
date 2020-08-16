import pytest
import json

def test_create(client, auth):
    authHeader = auth.header()
    response = client.post("/api/v1/classifier", data=json.dumps({"name": "TEST_CLASSIFIER2", "regex": [".*test.*"]}), headers=authHeader, content_type='application/json')
    assert response.status_code == 201

def test_create_without_auth(client):
    response = client.post("/api/v1/classifier", data=json.dumps({"name": "TEST_CLASSIFIER2", "regex": [".*test.*"]}), content_type='application/json')
    assert response.status_code == 401

@pytest.mark.parametrize(
    ("name", "regex", "message", "status"),
    (
        ("", "", "Parameter 'name' was not provided or is invalid", 400),
        ("TEST_CLASSIFIER", "", "Parameter 'regex' was not provided or is invalid", 400),
        ("TEST_CLASSIFIER", "test", "Parameter 'regex' was not provided or is invalid", 400),
        ("TEST_CLASSIFIER", [], "Parameter 'regex' should contain at least one element", 400),
        ("TEST_CLASSIFIER", ["test"], "There is already a classifier with the name provided", 409)
    )
)
def test_create_validate_input(client, auth, name, regex, message, status):
    authHeader = auth.header()
    response = client.post("/api/v1/classifier", data=json.dumps({"name": name, "regex": regex}), headers=authHeader, content_type='application/json')
    assert message == response.get_json().get("msg")
    assert status == response.status_code

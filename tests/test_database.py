import pytest
import json

def test_create(client, auth):
    authHeader = auth.header()
    response = client.post("/api/v1/database", data=json.dumps({"host": "test.host", "port": 3306, "username": "test", "password": "test"}), headers=authHeader, content_type='application/json')
    assert response.status_code == 201

def test_create_without_auth(client):
    response = client.post("/api/v1/database", data=json.dumps({"host": "test.host", "port": 3306, "username": "test", "password": "test"}), content_type='application/json')
    assert response.status_code == 401

@pytest.mark.parametrize(
    ("host", "port", "username", "password", "message", "status"),
    (
        ("", "", "", "", "Parameter 'host' was not provided or is invalid", 400),
        ("test.host", "", "", "", "Parameter 'port' was not provided or is invalid", 400),
        ("test.host", 3306, "", "", "Parameter 'username' was not provided or is invalid", 400),
        ("test.host", 3306, "test", "", "Parameter 'password' was not provided or is invalid", 400)
    )
)
def test_create_validate_input(client, auth, host, port, username, password, message, status):
    authHeader = auth.header()
    response = client.post("/api/v1/database", data=json.dumps({"host": host, "port": port, "username": username, "password": password}), headers=authHeader, content_type='application/json')
    assert message == response.get_json().get("msg")
    assert status == response.status_code

def test_start_scan_unexisting_database(client, auth):
    authHeader = auth.header()
    response = client.post("/api/v1/database/scan/test", headers=authHeader)
    assert response.status_code == 404
    assert response.get_json().get('msg') == "Database not found"

def test_start_scan_unreachable_database(client, auth):
    authHeader = auth.header()
    response = client.post("/api/v1/database", data=json.dumps({"host": "test.host", "port": 3308, "username": "root", "password": "test"}), headers=authHeader, content_type='application/json')
    database_id = response.get_json().get('_id')
    response = client.post("/api/v1/database/scan/{}".format(database_id), headers=authHeader)
    assert response.status_code == 502

def test_create_and_get_empty_scan(client, auth):
    authHeader = auth.header()
    response = client.post("/api/v1/database", data=json.dumps({"host": "test.host", "port": 3306, "username": "test", "password": "test"}), headers=authHeader, content_type='application/json')
    database_id = response.get_json().get('_id')
    response = client.get("/api/v1/database/scan/{}".format(database_id), headers=authHeader)
    assert response.status_code == 200
    assert response.get_json() == {}
    response = client.get("/api/v1/database/scan/{}/render".format(database_id), headers=authHeader)
    assert response.status_code == 200

def test_get_scan_unexisting_databse(client, auth):
    authHeader = auth.header()
    response = client.get("/api/v1/database/scan/1", headers=authHeader)
    assert response.status_code == 404
    assert response.get_json().get('msg') == 'Database not found'
    response = client.get("/api/v1/database/scan/1/render", headers=authHeader)
    assert response.status_code == 404
from base64 import b64encode
from io import BytesIO
from os import path, makedirs, remove, rmdir

import pytest

from app import app as flask_app
from utils.metadata import add_file_metadata


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    username, password = app.config["USER"]
    return app.test_client(), username, password


def test_upload_success(client, app):
    test_client, username, password = client
    data = {
        'the_file': (BytesIO(b"file content"), 'testfile.txt')
    }
    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }
    response = test_client.post('/upload', data=data, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 200
    assert len(response.data) == 64


def test_upload_no_file(client):
    test_client, username, password = client
    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }
    response = test_client.post('/upload', data={}, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 400


def test_download_file_success(client, app):
    test_client, username, password = client
    file_hash = "abcdef1234567890"
    file_dir = path.join(app.config["FILE_STORAGE_PATH"], file_hash[:2])
    file_path = path.join(file_dir, file_hash)
    makedirs(file_dir, exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Test file content.")

    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }
    response = test_client.get(f'/download/{file_hash}', headers=headers)
    assert response.status_code == 200
    assert response.data.decode() == "Test file content."

    remove(file_path)
    rmdir(file_dir)


def test_download_file_not_found(client):
    test_client, username, password = client
    file_hash = "nonexistentfilehash"

    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}'
    }
    response = test_client.get(f'/download/{file_hash}', headers=headers)
    assert response.status_code == 404


def test_delete_file_success(client, app):
    test_client, username, password = client
    file_hash = "deletefile12345678"
    file_dir = path.join(app.config["FILE_STORAGE_PATH"], file_hash[:2])
    file_path = path.join(file_dir, file_hash)
    makedirs(file_dir, exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Delete me")
    add_file_metadata(file_hash, username, file_path)

    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    response = test_client.delete(f'/delete/{file_hash}', headers=headers)
    assert response.status_code == 200
    assert not path.exists(file_path), "File should be deleted"


def test_delete_file_not_found(client):
    test_client, username, password = client
    file_hash = "nonexistentfilehash1234"

    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}

    response = test_client.delete(f'/delete/{file_hash}', headers=headers)
    assert response.status_code == 404


def test_delete_file_unauthorized(client, app):
    test_client, username, password = client
    file_hash = "unauthfile12345678"
    user_dir = path.join(app.config["FILE_STORAGE_PATH"], "other_user")
    file_dir = path.join(user_dir, file_hash[:2])
    file_path = path.join(file_dir, file_hash)
    makedirs(file_dir, exist_ok=True)
    with open(file_path, "w") as f:
        f.write("This is not your file")

    wrong_credentials = b64encode(f"wronguser:wrongpass".encode()).decode('utf-8')
    headers = {'Authorization': f'Basic {wrong_credentials}'}

    response = test_client.delete(f'/delete/{file_hash}', headers=headers)
    assert response.status_code == 401

    remove(file_path)
    rmdir(file_dir)
    rmdir(user_dir)

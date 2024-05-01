from base64 import b64encode
from io import BytesIO

import pytest

from app import app as flask_app


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

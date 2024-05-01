from io import BytesIO

import pytest

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_upload_success(client):
    data = {
        'the_file': (BytesIO(b"file content"), 'testfile.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert len(response.data) == 64


def test_upload_no_file(client):
    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400

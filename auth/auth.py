from flask_httpauth import HTTPBasicAuth

from app import app

auth = HTTPBasicAuth()

USERNAME, PASSWORD = app.config["USER"]


@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and password == PASSWORD:
        return username

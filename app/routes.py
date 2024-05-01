import hashlib
import os

from flask import request, send_from_directory, abort, Response

from app import app
from auth.auth import auth


@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    file = request.files['the_file']
    if file and file.filename != "":
        file_content = file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        file_dir = os.path.join(app.config["FILE_STORAGE_PATH"], file_hash[:2])
        file_path = os.path.join(file_dir, file_hash)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_content)
        return file_hash


@app.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash: str) -> Response:
    file_dir = os.path.join(app.config["FILE_STORAGE_PATH"], file_hash[:2])
    file_path = os.path.join(file_dir, file_hash)
    if os.path.exists(file_path):
        return send_from_directory(directory=file_dir, path=file_hash, as_attachment=True)
    else:
        abort(404, description="File not found")

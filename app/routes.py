import hashlib
import os

from flask import request, send_from_directory, abort, Response

from app import app
from auth.auth import auth
from utils.metadata import add_file_metadata, load_metadata, delete_file_metadata


@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    username = request.authorization.username
    file = request.files['the_file']
    if file and file.filename != "":
        file_content = file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        file_dir = os.path.join(app.config["FILE_STORAGE_PATH"], file_hash[:2])
        file_path = os.path.join(file_dir, file_hash)
        os.makedirs(file_dir, exist_ok=True)
        add_file_metadata(file_hash, username, file_path)
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


@app.route('/delete/<file_hash>', methods=['DELETE'])
@auth.login_required
def delete_file(file_hash: str):
    username = request.authorization.username
    metadata = load_metadata()
    if file_hash in metadata and metadata[file_hash]['owner'] == username:
        os.remove(metadata[file_hash]['path'])
        delete_file_metadata(file_hash)
        return {"message": "File deleted successfully"}, 200
    else:
        abort(404, "File not found or access denied")

import hashlib
import os

from flask import request

from app import app


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['the_file']
    if file and file.filename != "":
        file_content = file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        file_dir = os.path.join(app.config["FILE_STORAGE_PATH"], file_hash[:3])
        file_path = os.path.join(file_dir, file_hash)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_content)
        return file_hash

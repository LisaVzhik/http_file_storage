import os

from dotenv import load_dotenv
from flask import Flask
from utils.logger import setup_logger

load_dotenv()
setup_logger()

app = Flask(__name__)

app.config["FILE_STORAGE_PATH"] = os.getenv("FILE_STORAGE_PATH")
app.config["USER"] = (os.getenv("USERNAME"), os.getenv("PASSWORD"))

if not app.config["FILE_STORAGE_PATH"]:
    raise ValueError("FILE_STORAGE_PATH must be set in the env")

from .routes import upload_file, download_file, delete_file

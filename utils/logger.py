from loguru import logger
from os import path, makedirs


def setup_logger():
    log_dir = "logs"
    if not path.exists(log_dir):
        makedirs(log_dir)

    log_filepath = path.join(log_dir, "http_file_storage.log")
    logger.add(log_filepath, rotation="20mb", level="INFO")

    error_log_filepath = path.join(log_dir, "errors.log")
    logger.add(error_log_filepath, rotation="20mb", level="ERROR")

    logger.info("Logging startup")

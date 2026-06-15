import os
import sys
import logging

def setup_logger(tool_name: str) -> logging.Logger:
    logger = logging.getLogger(tool_name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(levelname)s: %(message)s")

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

    return logger

def print_exception(logger: logging.Logger) -> None:
    exc_type, exc_value, _ = sys.exc_info()
    logger.error(f"{exc_type.__name__}: {exc_value}")

def make_path_unique(path: str) -> str:
    name, extension = os.path.splitext(path)
    unique_path = path
    counter = 1

    while os.path.exists(unique_path):
        unique_path = f"{name} ({counter}){extension}"
        counter += 1

    return unique_path

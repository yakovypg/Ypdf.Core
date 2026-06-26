# pip install tika==3.1.0
# Java 11+ required

import os
import sys
import time
import argparse
import threading
import subprocess

from typing import Tuple
from urllib.request import urlopen

from Utils import setup_logger, print_exception

TOOL_NAME = "TextExtractor"
logger = setup_logger(TOOL_NAME)

def pipe_to_logger(stream, prefix: str):
    try:
        for line in iter(stream.readline, ""):
            if not line:
                break

            logger.info(f"{prefix}{line.rstrip()}")
    finally:
        try:
            stream.close()
        except Exception:
            pass

def start_tika_server(
    tika_server_jar_path: str,
    classpath: str,
    host: str,
    port: int
) -> Tuple[subprocess.Popen, threading.Thread]:
    if not os.path.isfile(tika_server_jar_path):
        raise FileNotFoundError(f"Tika server jar not found: {tika_server_jar_path}")

    cmd = [
        "java", "-cp", tika_server_jar_path,
        classpath,
        "--host", host,
        "--port", str(port),
    ]

    tika_server_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    tika_server_logger_thread = threading.Thread(
        target=pipe_to_logger,
        args=(tika_server_process.stdout, "[tika] "),
        daemon=True
    )

    tika_server_logger_thread.start()

    return (tika_server_process, tika_server_logger_thread)

def terminate_tika_server(tika_server_process: subprocess.Popen, timeout_s: float = 5.0) -> None:
    if tika_server_process is None:
        return

    try:
        tika_server_process.terminate()
        tika_server_process.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        tika_server_process.kill()
        tika_server_process.wait()

def wait_tika_server(tika_server_url: str, timeout_s: float = 10.0) -> None:
    RETRY_CONNECTION_TIMEOUT_S = 1
    URL_OPEN_TIMEOUT_S = 1

    deadline = time.time() + timeout_s

    while time.time() < deadline:
        try:
            with urlopen(tika_server_url, timeout=URL_OPEN_TIMEOUT_S) as reader:
                reader.read(1)

            return
        except Exception as e:
            logger.info(f"Failed to connect to tika server: {e}")
            logger.info(f"Retry connection after {RETRY_CONNECTION_TIMEOUT_S} seconds")
            time.sleep(RETRY_CONNECTION_TIMEOUT_S)

    raise RuntimeError("Failed to connect to tika server")

def prepare_tika_server(tika_server_jar_path: str) -> Tuple[subprocess.Popen, threading.Thread]:
    if not os.path.isfile(tika_server_jar_path):
        raise FileNotFoundError(f"Tika server jar not found: {tika_server_jar_path}")

    TIKA_SERVER_CLASSPATH = "org.apache.tika.server.core.TikaServerCli"
    TIKA_SERVER_HOST = "127.0.0.1"
    TIKA_SERVER_PORT = 9998
    TIKA_SERVER_URL = f"http://{TIKA_SERVER_HOST}:{TIKA_SERVER_PORT}"

    tika_server_process, tika_server_logger_thread = start_tika_server(
        tika_server_jar_path,
        TIKA_SERVER_CLASSPATH,
        TIKA_SERVER_HOST,
        TIKA_SERVER_PORT)

    wait_tika_server(TIKA_SERVER_URL)

    os.environ["TIKA_CLIENT_ONLY"] = "True"
    os.environ["TIKA_SERVER_ENDPOINT"] = TIKA_SERVER_URL

    return (tika_server_process, tika_server_logger_thread)

def extract_text(input_path: str, output_path: str, tika_server_jar_path: str = None) -> None:
    tika_server_process = None

    if tika_server_jar_path:
        tika_server_process, _ = prepare_tika_server(tika_server_jar_path)

    from tika import parser

    parsed_file = parser.from_file(input_path)
    content = parsed_file.get("content") or ""

    with open(output_path, "w", encoding="utf-8") as writer:
        writer.write(content)
        logger.info(f"Saved: {output_path}")

    if tika_server_process is not None:
        terminate_tika_server(tika_server_process)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = TOOL_NAME,
        description="script for extracting text from PDF document")

    parser.add_argument(
        "-i",
        "--input-path",
        help="path to the PDF document from which text will be extracted",
        type=str,
        required=True)

    parser.add_argument(
        "-o",
        "--output-path",
        help="path to the file where the text will be saved",
        type=str,
        required=True)

    parser.add_argument(
        "-j",
        "--tika-jar",
        help="path to the tika server .jar file",
        type=str,
        default=None)

    return parser

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        extract_text(args.input_path, args.output_path, args.tika_jar)
        return 0
    except Exception:
        print_exception(logger)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

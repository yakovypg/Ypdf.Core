# pip install tika==3.1.0

import sys
import argparse

from tika import parser
from Utils import setup_logger, print_exception, make_path_unique

TOOL_NAME = "TextExtractor"
logger = setup_logger(TOOL_NAME)

def extract_text(input_path: str, output_path: str) -> None:
    parsed_file = parser.from_file(input_path)
    content = parsed_file.get("content") or ""

    with open(output_path, "w", encoding="utf-8") as writer:
        writer.write(content)
        logger.info(f"Saved: {output_path}")

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

    return parser

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        extract_text(args.input_path, args.output_path)
        return 0
    except Exception:
        print_exception(logger)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

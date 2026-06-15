# pip install pdf2image==1.17.0

import os
import sys
import argparse

from pdf2image import convert_from_path
from Utils import setup_logger, print_exception, make_path_unique

TOOL_NAME = "PdfRenderer"
logger = setup_logger(TOOL_NAME)

def render_pdf(
    pdf_path: str,
    output_directory: str,
    img_extension: str = "png",
    dpi: int = 150,
    pages: list[int] = None
) -> None:
    output_directory = output_directory or "."

    file_basename = os.path.basename(pdf_path)
    file_name = os.path.splitext(file_basename)[0]

    def save_image(img, page_num: int, img_extension: str = "png"):
        img_name = f"{file_name}_p{page_num}.{img_extension}"
        img_path = make_path_unique(os.path.join(output_directory, img_name))

        img.save(img_path)
        logger.info(f"Saved: {img_path}")

    if pages is not None and len(pages) > 0:
        for page_num in pages:
            images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num)

            if not images or len(images) == 0:
                continue

            img = images[0]
            save_image(img, page_num, img_extension)
    else:
        images = convert_from_path(pdf_path, dpi=dpi)

        for page_num, img in enumerate(images, start=1):
            save_image(img, page_num, img_extension)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=TOOL_NAME, description="script to render PDF pages to images")

    parser.add_argument(
        "-i",
        "--input-path",
        help="path to the PDF document which pages will be rendered",
        type=str,
        required=True)

    parser.add_argument(
        "-o",
        "--output-directory",
        help="path to the directory for saving images",
        type=str,
        default="")

    parser.add_argument(
        "-e",
        "--extension",
        help="output images extension. Default is PNG",
        type=str,
        default="png")

    parser.add_argument(
        "-d",
        "--dpi",
        help="output images DPI. Default is 150",
        type=int,
        default=150)

    parser.add_argument(
        "-p",
        "--pages",
        nargs="*",
        help="pages that will be rendered. Omit to render all pages",
        default=None,
    )

    return parser

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        pages = [int(p) for p in args.pages or []]
        render_pdf(args.input_path, args.output_directory, args.extension, args.dpi, pages)
        return 0
    except Exception:
        print_exception(logger)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

# pip install PyMuPDF==1.27.2.2

import os
import sys
import fitz
import argparse

from Utils import setup_logger, print_exception, make_path_unique

TOOL_NAME = "ImageExtractor"
logger = setup_logger(TOOL_NAME)

def extract_images(pdf_path: str, output_directory: str, imgs_count_limit: int = 0) -> None:
    output_directory = output_directory or "."
    limit = imgs_count_limit if imgs_count_limit and imgs_count_limit > 0 else None

    try:
        file_basename = os.path.basename(pdf_path)
        file_name = os.path.splitext(file_basename)[0]

        img_num = 0

        with fitz.open(pdf_path) as doc:
            total_pages = len(doc)

            for page_index in range(total_pages):
                page_number = page_index + 1
                logger.debug(f"Processing {file_basename}: page {page_number}/{total_pages}")

                page = doc.load_page(page_index)
                image_list = page.get_images(full=True)

                if not image_list:
                    logger.debug(f"No images on page {page_number} of {file_basename}")
                    continue

                for img_info in image_list:
                    xref = img_info[0]

                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        img_ext = base_image.get("ext", "png").lower()

                        img_num += 1

                        img_name = f"{file_name}_p{page_number}_r{xref}_n{img_num}.{img_ext}"
                        img_path = make_path_unique(os.path.join(output_directory, img_name))

                        with open(img_path, "wb") as img_file:
                            img_file.write(image_bytes)

                        logger.info(f"Saved: {img_path}")

                        if limit is not None and img_num >= limit:
                            raise StopIteration
                    except StopIteration:
                        raise
                    except Exception as e:
                        logger.debug(f"Failed to extract image xref={xref} from {file_basename}: {e}")
    except StopIteration:
        logger.info("Image limit reached")
    except Exception:
        print_exception(logger)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="script for extracting embedded images from PDF documents")

    parser.add_argument(
        "-i",
        "--input-path",
        help="path to the PDF document which images will be extracted from",
        type=str,
        required=True)

    parser.add_argument(
        "-o",
        "--output-directory",
        help="path to the directory for saving extracted images",
        type=str,
        default=None)

    parser.add_argument(
        "-l",
        "--limit",
        help="maximum number of images to extract (0 = no limit)",
        type=int,
        default=0)

    return parser

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        extract_images(args.input_path, args.output_directory, args.limit)
        return 0
    except Exception:
        print_exception(logger)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

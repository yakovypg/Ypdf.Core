# pip install pillow==12.1.1

import os
import sys
import argparse

from PIL import Image
from Utils import setup_logger, print_exception, make_path_unique

TOOL_NAME = "ImageCompressor"
logger = setup_logger(TOOL_NAME)

def get_formatted_size(bytes_value: float, factor: int = 1024, suffix: str = "B") -> str:
    for prefix in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if bytes_value < factor:
            return f"{bytes_value:.2f} {prefix}{suffix}"

        bytes_value /= factor

    return f"{bytes_value:.2f}Y{suffix}"

def compress_image(
    image_path: str,
    output_path: str,
    quality_factor: float = 0.75,
    size_factor: float = 1.0,
    new_width: int = None,
    new_height: int = None,
) -> None:
    img = Image.open(image_path)

    source_img_size = img.size
    source_img_size_str = f"{source_img_size[0]}x{source_img_size[1]}"
    source_img_weight = os.path.getsize(image_path)
    source_img_weight_str = get_formatted_size(source_img_weight)

    output_img_size = img.size

    if new_width or new_height:
        new_width = new_width if new_width else img.size[0]
        new_height = new_height if new_height else img.size[1]
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        output_img_size = img.size
    elif size_factor is not None and size_factor != 1.0:
        new_width = max(1, int(img.size[0] * size_factor))
        new_height = max(1, int(img.size[1] * size_factor))
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        output_img_size = img.size

    quality = int(max(0.01, min(1.0, quality_factor)) * 100)

    try:
        img.save(output_path, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(output_path, quality=quality, optimize=True)

    output_img_size_str = f"{output_img_size[0]}x{output_img_size[1]}"
    output_img_weight = os.path.getsize(output_path)
    output_img_weight_str = get_formatted_size(output_img_weight)

    compression = (1 - output_img_weight / source_img_weight) * 100 if source_img_weight > 0 else 0.0
    compression_str = f"{compression:.2f}%"

    source_img_name = os.path.basename(image_path)

    logger.info(f"image: {source_img_name}")
    logger.info(f"size: {source_img_size_str} -> {output_img_size_str}")
    logger.info(f"weight: {source_img_weight_str} -> {output_img_weight_str}")
    logger.info(f"compression: {compression_str}")

def compress_images(
    image_paths: list[str],
    output_directory: str,
    quality_factor: float = 0.75,
    size_factor: float = 1.0,
    extension: str = None,
) -> None:
    output_directory = output_directory or "."

    for i, image_path in enumerate(image_paths):
        img_basename = os.path.basename(image_path)
        img_name = os.path.splitext(img_basename)[0]
        img_extension = os.path.splitext(image_path)[1] or ".jpg"

        if extension:
            img_extension = extension if extension.startswith(".") else f".{extension}"

        unique_path = os.path.join(output_directory, f"{img_name}_compressed{img_extension}")
        unique_path = make_path_unique(unique_path)

        compress_image(image_path, unique_path, quality_factor, size_factor)

        if i < len(image_paths) - 1:
            logger.info("")

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = TOOL_NAME,
        description="script for compressing images")

    parser.add_argument(
        "-i",
        "--input-images",
        nargs="+",
        help="images to compress",
        type=str,
        required=True)

    parser.add_argument(
        "-o",
        "--output-path",
        help=("path to the compressed image or path to the directory for saving compressed " +
             "images if several input images specified"),
        type=str,
        default=None)

    parser.add_argument(
        "-e",
        "--extension",
        help="extension in which the images will be converted",
        type=str,
        default=None)

    parser.add_argument(
        "-q",
        "--quality",
        help="output image quality [from 0.0 (worst) to 0.95 (best)]. Default is 0.75",
        type=float,
        default=0.75)

    parser.add_argument(
        "-s",
        "--size-factor",
        help="resizing factor (setting to X will multiply width & height by X). Default is 1.0",
        type=float,
        default=1.0)

    parser.add_argument(
        "-W",
        "--width",
        help="new width of the image",
        type=int,
        default=None)

    parser.add_argument(
        "-H",
        "--height",
        help="new height of the image",
        type=int,
        default=None)

    return parser

def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        if len(args.input_images) == 1:
            compress_image(
                args.input_images[0],
                args.output_path,
                args.quality,
                args.size_factor,
                args.width,
                args.height)
        else:
            compress_images(
                args.input_images,
                args.output_path,
                args.quality,
                args.size_factor,
                args.extension)

        return 0
    except Exception:
        print_exception(logger)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

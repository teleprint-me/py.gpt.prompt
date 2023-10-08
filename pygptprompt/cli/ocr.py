"""
pygptprompt/ocr.py

A command-line OCR tool that performs various image processing operations and extracts text from images.
"""

import click

from pygptprompt.processor.image import ImageProcessor


@click.command()
@click.option(
    "--path_image",
    prompt="File path to input image",
    help="The file path to the input image.",
)
@click.option(
    "--path_text",
    default="",
    help="The file path to save the extracted text. Default is an empty string (print to console).",
)
@click.option(
    "--rotate",
    default=0,
    help="Rotate the image by the specified angle in degrees. Default is 0.",
)
@click.option(
    "--scale",
    default=0,
    help="Scale the image by the specified factor. Default is 0.",
)
@click.option("--grayscale", is_flag=True, help="Convert the image to grayscale.")
@click.option("--contrast", is_flag=True, help="Enhance the image contrast.")
@click.option(
    "--burn",
    is_flag=True,
    help="Burn the image by adjusting brightness and contrast.",
)
@click.option(
    "--preprocess",
    is_flag=True,
    help="Preprocess the image for text extraction using adaptive thresholding and erosion-dilation.",
)
@click.option(
    "--contours",
    is_flag=True,
    help="Extract text from image using contours and bounding rectangular areas.",
)
def main(
    path_image,
    path_text,
    rotate,
    scale,
    grayscale,
    contrast,
    burn,
    preprocess,
    contours,
):
    """
    Perform image processing operations and extract text from images.
    """
    processor = ImageProcessor(path_image)

    if rotate:
        processor.rotate_image(rotate)

    if scale:
        processor.scale_image(scale)

    if grayscale:
        processor.grayscale_image()

    if contrast:
        processor.contrast_image()

    if burn:
        processor.burn_image()

    if preprocess:
        processor.preprocess_image()

    if contours:
        text = processor.extract_text_from_image_contours()
    else:
        text = processor.extract_text_from_image()

    if path_text:
        with open(path_text, "w") as plaintext:
            plaintext.writelines(text.splitlines())
    else:
        print(text)


if __name__ == "__main__":
    main()

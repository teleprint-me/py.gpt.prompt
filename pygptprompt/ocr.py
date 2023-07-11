"""
pygptprompt/ocr.py

https://docs.opencv.org/4.x/
https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
"""
import click

from pygptprompt.processor.image import ImageProcessor


@click.command()
@click.option(
    "--path_image",
    prompt="File path to input image",
    help="The file path to the given input image.",
)
@click.option(
    "--path_text",
    default=str(),
    help="The file path for the given text output. Default is empty string.",
)
@click.option(
    "--rotate",
    default=0,
    help="Rotate the image by a given angle. Default is 0.",
)
@click.option(
    "--scale",
    default=0,
    help="Scale the image by a given factor. Default is 0.",
)
@click.option("--grayscale", is_flag=True, help="Convert image to grayscale.")
@click.option("--contrast", is_flag=True, help="Increase image contrast.")
@click.option("--burn", is_flag=True, help="Burn the image by decreasing brightness.")
@click.option(
    "--preprocess",
    is_flag=True,
    help="Preprocess image using a binary gaussian-weighted sum and dilation.",
)
@click.option(
    "--contours",
    is_flag=True,
    help="Add contours to the image using bound rectangular areas.",
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

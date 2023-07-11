"""
pygptprompt/ocr.py

https://docs.opencv.org/4.x/
https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
"""
import click
import cv2
import numpy as np
import pytesseract


class ImageProcessor:
    def __init__(self, file_path):
        self.image, self.base_image = self.load_image(file_path)

    def load_image(self, file_path):
        image = cv2.imread(file_path)
        base_image = image.copy()
        return image, base_image

    def add_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def scale_image(self):
        height, width = self.image.shape[:2]
        self.image = cv2.resize(
            self.image,
            (int(width * 1.5), int(height * 1.5)),
            interpolation=cv2.INTER_AREA,
        )

    def increase_contrast(self):
        self.image = cv2.equalizeHist(self.image)

    def preprocess_image(self):
        binary = cv2.adaptiveThreshold(
            self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        self.image = cv2.erode(dilated, kernel, iterations=1)

    def rotate_image(self, angle):
        height, width = self.image.shape[:2]
        image_center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1)
        self.image = cv2.warpAffine(self.image, rotation_matrix, (width, height))

    def find_contours(self):
        contours, _ = cv2.findContours(
            self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])
        extracted_text = ""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = self.base_image[y : y + h, x : x + w]
            extracted_text += pytesseract.image_to_string(roi)
        return extracted_text

    def extract_text(self, image):
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text


@click.command()
@click.option("--path", prompt="Path to image", help="The path to the image.")
@click.option("--rotate", default=0, help="Rotate image by a certain angle.")
@click.option("--scale", is_flag=True, help="Scale image.")
@click.option("--grayscale", is_flag=True, help="Convert image to grayscale.")
@click.option("--contrast", is_flag=True, help="Increase image contrast.")
@click.option(
    "--preprocess",
    is_flag=True,
    help="Preprocess image using a binary gaussian-weighted sum and dilation.",
)
@click.option(
    "--contours",
    is_flag=True,
    help="Add contours to the image using a bound rectangular area.",
)
def main(
    path,
    rotate,
    scale,
    grayscale,
    contrast,
    preprocess,
    contours,
):
    processor = ImageProcessor(path)

    if rotate:
        processor.rotate_image(rotate)

    if scale:
        processor.scale_image()

    if grayscale:
        processor.add_grayscale()

    if contrast:
        processor.increase_contrast()

    if preprocess:
        processor.preprocess_image()

    if contours:
        text = processor.find_contours()
    else:
        text = processor.extract_text()

    print(text)


if __name__ == "__main__":
    main()

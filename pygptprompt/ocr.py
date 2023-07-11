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
    def __init__(self, file_path: str) -> None:
        """
        Initialize an ImageProcessor object.

        Parameters:
        - file_path: The path to the image file.

        This method loads the image file specified by `file_path` and creates two copies
        of it: `self.image` and `self.base_image`.
        """
        self.image, self.base_image = self.load_image(file_path)

    def load_image(self, file_path: str) -> tuple[np.ndarray, np.ndarray]:
        """
        Load an image from a file.

        Parameters:
        - file_path: The path to the image file.

        Returns:
        - image: The loaded image.
        - base_image: A copy of the loaded image.

        This method uses OpenCV's `imread` function to read the image file from `file_path`.
        It creates a copy of the image and returns both the image and the copy.
        """
        image = cv2.imread(file_path)
        base_image = image.copy()
        return image, base_image

    def grayscale_image(self) -> None:
        """
        Convert the image to grayscale.

        This method applies the BGR to grayscale conversion using OpenCV's `cvtColor`
        function and updates `self.image` with the grayscale version.
        """
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def scale_image(self, n: float) -> None:
        """
        Scale the image by a factor.

        Parameters:
        - n: The scaling factor.

        This method resizes the image dimensions proportionally based on the given scaling
        factor `n` using OpenCV's `resize` function with the interpolation method set to
        `cv2.INTER_AREA`. It updates `self.image` with the scaled version.
        """
        height, width = self.image.shape[:2]
        self.image = cv2.resize(
            self.image,
            (int(width * n), int(height * n)),
            interpolation=cv2.INTER_AREA,
        )

    def rotate_image(self, angle: float) -> None:
        """
        Rotate the image.

        Parameters:
        - angle: The rotation angle in degrees.

        This method rotates the image by the specified angle around its center using
        OpenCV's `getRotationMatrix2D` and `warpAffine` functions. It updates `self.image`
        with the rotated version.
        """
        height, width = self.image.shape[:2]
        image_center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1)
        self.image = cv2.warpAffine(self.image, rotation_matrix, (width, height))

    def contrast_image(self) -> None:
        """
        Enhance the image contrast.

        This method improves the contrast of the image by applying histogram equalization
        using OpenCV's `equalizeHist` function. It updates `self.image` with the enhanced
        version.
        """
        self.image = cv2.equalizeHist(self.image)

    def burn_image(self, alpha: float = 1.0, beta: int = -50) -> None:
        """
        Burn an image by adjusting brightness and contrast.

        Parameters:
        - alpha: The contrast control (1.0-3.0).
        - beta: The brightness control (-50 to 50).

        This method adjusts the brightness and contrast of the image using OpenCV's
        `convertScaleAbs` function with the specified alpha and beta values. It updates
        `self.image` with the modified version.
        """
        self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)

    def preprocess_image(self) -> None:
        """
        Preprocess the image for text extraction.

        This method applies adaptive thresholding, dilation, and erosion operations to the
        image using OpenCV's `adaptiveThreshold`, `dilate`, and `erode` functions. It
        updates `self.image` with the preprocessed version.
        """
        binary = cv2.adaptiveThreshold(
            self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        self.image = cv2.erode(dilated, kernel, iterations=1)

    def find_contours_and_extract_text(self) -> str:
        """
        Find contours in the image and extract text from regions.

        Returns:
        - extracted_text: The extracted text from the image.

        This method uses OpenCV's `findContours` function to detect contours in the image.
        The contours are sorted based on their y-coordinate, and text is extracted from
        each contour region using pytesseract's `image_to_string` function. The extracted
        text is returned as a single string.
        """
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

    @staticmethod
    def extract_text(image: np.ndarray) -> str:
        """
        Extract text from an image.

        Parameters:
        - image: The input image.

        Returns:
        - extracted_text: The extracted text from the image.

        This static method uses pytesseract's `image_to_string` function to extract text
        from the given image and returns it as a string.
        """
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text


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
        text = processor.find_contours_and_extract_text()
    else:
        text = processor.extract_text()

    if path_text:
        with open(path_text, "w") as plaintext:
            plaintext.writelines(text.splitlines())
    else:
        print(text)


if __name__ == "__main__":
    main()

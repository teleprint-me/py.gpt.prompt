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

    def extract_text(self):
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


def main():
    # Load the image
    image, base_image = load_image("data/Arithmetic-Scanned-Document.jpg")

    # Convert the image to grayscale
    gray = add_grayscale(image)

    # Scale the image
    scaled = scale_image(gray)

    # Increase contrast
    contrasted = increase_contrast(scaled)

    # Preprocess the image
    preprocessed = preprocess_image(contrasted)

    # Extract text
    extracted_text = extract_text(preprocessed, base_image)

    # Print the extracted text
    print(extracted_text)


if __name__ == "__main__":
    main()

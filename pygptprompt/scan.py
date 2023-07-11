import cv2
import numpy as np
import pytesseract


def load_image(file_path):
    # Load the image
    image = cv2.imread(file_path)  # "flags=0 == grayscale"?
    base_image = image.copy()
    return image, base_image


def convert_to_grayscale(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def scale_image(image):
    # Calculate the new dimensions of the image
    width = int(image.shape[1] * 1.5)  # increase width by 50%
    height = int(image.shape[0] * 1.5)  # increase height by 50%
    dim = (width, height)

    # Resize the image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def increase_contrast(image):
    # Apply histogram equalization
    equalized = cv2.equalizeHist(image)
    return equalized


def preprocess_image(image):
    # Apply adaptive thresholding to convert the image to binary
    binary = cv2.adaptiveThreshold(
        src=image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2,  # constant subtracted from weighted mean
    )

    # Create a kernel for dilation and erosion
    kernel = np.ones((1, 1), np.uint8)

    # Use dilation and erosion to remove noise
    dilated = cv2.dilate(binary, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    return eroded


def extract_text(image, base_image):
    # Find contours
    contours, _ = cv2.findContours(
        image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    # Sort contours by their y-position (top to bottom)
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

    # Initialize an empty string to hold the extracted text
    extracted_text = ""

    # Iterate over the contours
    for contour in contours:
        # Get the bounding box coordinates (x, y)
        # and the width and height (w, h)
        x, y, w, h = cv2.boundingRect(contour)

        # Extract the region of interest (ROI) from the base image
        roi = base_image[y : y + h, x : x + w]

        # Convert the ROI to text using pytesseract and append
        # it to the extracted_text string
        extracted_text += pytesseract.image_to_string(roi)

    return extracted_text


def main():
    # Load the image
    image, base_image = load_image("data/Arithmetic-Scanned-Document.jpg")

    # Convert the image to grayscale
    gray = convert_to_grayscale(image)

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

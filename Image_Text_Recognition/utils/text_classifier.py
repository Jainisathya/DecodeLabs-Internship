import easyocr
from PIL import Image
import numpy as np
import cv2

# Load EasyOCR model only once
reader = easyocr.Reader(['en'], gpu=False)

def read_text(image_path):
    """
    Extract text from an image using EasyOCR.

    Returns:
        extracted_text (str)
        average_confidence (float)
        detection_count (int)
    """

    image = cv2.imread(image_path)

    if image is None:
        return "Unable to read image.", 0, 0

    results = reader.readtext(image)

    extracted_text = ""

    confidences = []

    for detection in results:

        bbox, text, confidence = detection

        extracted_text += text + "\n"

        confidences.append(confidence)

    if len(confidences) == 0:
        avg_confidence = 0
    else:
        avg_confidence = sum(confidences) / len(confidences)

    return extracted_text.strip(), avg_confidence * 100, len(results)


def draw_boxes(image_path):

    """
    Draw bounding boxes around detected text.
    Returns OpenCV image.
    """

    image = cv2.imread(image_path)

    results = reader.readtext(image)

    for detection in results:

        bbox, text, confidence = detection

        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))

        cv2.rectangle(
            image,
            top_left,
            bottom_right,
            (0,255,0),
            2
        )

        cv2.putText(
            image,
            text,
            (top_left[0], top_left[1]-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image
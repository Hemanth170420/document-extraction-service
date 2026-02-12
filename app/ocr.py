from paddleocr import PaddleOCR
import os
from app.utils import pdf_to_images

# Initialize OCR model once (efficient)
ocr = PaddleOCR(use_angle_cls=True, lang="en")


def run_ocr(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text_output = ""

    try:
        # Convert PDF → images
        if file_path.lower().endswith(".pdf"):
            images = pdf_to_images(file_path)
        else:
            images = [file_path]

        # Run OCR on each page/image
        for img in images:

            results = ocr.ocr(img, cls=True)

            if results is None:
                continue

            for line in results:
                for word in line:

                    text = word[-1][0]
                    confidence = word[-1][1]

                    text_output += f"{text} (conf:{confidence:.2f})\n"

    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {str(e)}")

    return text_output

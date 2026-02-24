from paddleocr import PaddleOCR
from app.utils import pdf_to_images

ocr = PaddleOCR(use_angle_cls=True, lang="en")


def run_ocr(file_path):
    text_output = ""

    if file_path.lower().endswith(".pdf"):
        images = pdf_to_images(file_path)
    else:
        images = [file_path]

    for img in images:
        results = ocr.ocr(img, cls=True)

        if results is None:
            continue

        for line in results[0]:  # Proper line grouping
            line_text = line[1][0]  # Extract text only
            text_output += line_text + "\n"

        text_output += "\n"

    return text_output
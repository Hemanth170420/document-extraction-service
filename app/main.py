import sys
import os
from app.ocr import run_ocr


def main(path):

    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    try:
        text = run_ocr(path)

        print("\n===== OCR OUTPUT =====\n")
        print(text)

        # Save raw OCR text
        with open("output/raw_text.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("\nSaved raw OCR output → output/raw_text.txt")

    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app/main.py <file_path>")
        sys.exit()

    file_path = sys.argv[1]
    main(file_path)

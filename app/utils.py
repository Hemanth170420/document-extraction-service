from pdf2image import convert_from_path
import os


def pdf_to_images(pdf_path, output_folder="temp_images"):

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_folder, exist_ok=True)

    try:
        images = convert_from_path(pdf_path, dpi=300)

        image_paths = []

        for i, img in enumerate(images):
            path = os.path.join(output_folder, f"page_{i}.png")
            img.save(path, "PNG")
            image_paths.append(path)

        if len(image_paths) == 0:
            raise ValueError("No pages found in PDF.")

        return image_paths

    except Exception as e:
        raise RuntimeError(f"PDF conversion failed: {str(e)}")

import re


def normalize_text(text):
    """
    Basic normalization to handle OCR noise.
    Converts to lowercase and removes extra spaces.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


def classify_document(text):

    text = normalize_text(text)

    # --------------------------------------------------
    # 1️⃣ Strong Heading Detection (High Confidence)
    # --------------------------------------------------
    if "packing list" in text:
        return "packing_list", 100

    # Make sure invoice detection does not falsely trigger
    if "invoice" in text and "packing list" not in text:
        return "invoice", 100

    # --------------------------------------------------
    # 2️⃣ Weighted Keyword Scoring (Fallback)
    # --------------------------------------------------

    invoice_keywords = {
        "invoice no": 3,
        "tax invoice": 3,
        "gst": 2,
        "bill to": 2,
        "amount due": 2,
        "total amount": 2,
        "subtotal": 1
    }

    packing_keywords = {
        "po number": 2,
        "order number": 2,
        "consignee": 3,
        "shipment": 2,
        "ship to": 2,
        "total cartons": 2,
        "gross weight": 2,
        "quantity": 1
    }

    invoice_score = sum(weight for word, weight in invoice_keywords.items() if word in text)
    packing_score = sum(weight for word, weight in packing_keywords.items() if word in text)

    # --------------------------------------------------
    # 3️⃣ Decision Logic
    # --------------------------------------------------
    if invoice_score > packing_score:
        return "invoice", invoice_score

    elif packing_score > invoice_score:
        return "packing_list", packing_score

    else:
        return "unknown", 0

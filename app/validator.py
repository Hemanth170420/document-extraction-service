def validate_invoice(data):

    warnings = []

    if not data.get("invoice_number"):
        warnings.append("Invoice number not detected")

    if not data.get("invoice_date"):
        warnings.append("Invoice date not detected")

    if not data.get("line_items"):
        warnings.append("No line items detected")

    return warnings


def validate_packing(data):

    warnings = []

    if not data.get("po_number"):
        warnings.append("PO number not detected")

    if not data.get("ship_to_address"):
        warnings.append("Ship-to address not detected")

    if not data.get("line_items"):
        warnings.append("No line items detected")

    return warnings
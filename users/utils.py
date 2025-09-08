import re


def upi_validation(upi_id):
    pattern = r"^[\w.-]+@[\w.-]+$"
    return re.match(pattern, upi_id) is not None

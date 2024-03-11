import re
from datetime import datetime


def is_only_digits(input_string):
    return bool(re.fullmatch(r'\d*', input_string))

def validate_npi(npi):
    return is_only_digits(npi) and len(npi) == 10

def is_only_digits(input_string):
    return bool(re.fullmatch(r'\d*', input_string))

def validate_npi(npi):
    return is_only_digits(npi) and len(npi) == 10

def validate_inputs(test_data):
    """
    Validate the input data against specified constraints.

    Args:
    - test_data (dict): A dictionary containing input data to be validated.

    Returns:
    - dict: A dictionary containing the validation result with the following keys:
        - "success" (bool): Indicates whether the input is valid (True) or not (False).
        - "message" (str): Descriptive message indicating the outcome of the validation.
        - "status_code" (int): HTTP status code indicating the outcome of the validation.
    """
    npi_length = 10  # NPI length constraint

    # Check if NPI field is present and validate its format
    npi_value = test_data.get("NPI", "")
    if not npi_value:
        return {
            "success": False,
            "message": "NPI field is missing.",
            "status_code": 400,
        }

    # Validate NPI length
    if len(str(npi_value)) != npi_length:
        return {
            "success": False,
            "message": f"NPI must be exactly {npi_length} digits.",
            "status_code": 400,
        }

    # Check FirstName field
    first_name = test_data.get("FirstName", "").strip()
    if not first_name:
        return {
            "success": False,
            "message": "First name is required.",
            "status_code": 400,
        }

    # Check if FirstName has leading or trailing spaces
    if first_name != test_data["FirstName"].strip():
        return {
            "success": False,
            "message": "First name cannot contain leading or trailing spaces.",
            "status_code": 400,
        }

    # Check LastName field
    last_name = test_data.get("LastName", "").strip()
    if not last_name:
        return {
            "success": False,
            "message": "Last name is required.",
            "status_code": 400,
        }

    # Check if LastName has leading or trailing spaces
    if last_name != test_data["LastName"].strip():
        return {
            "success": False,
            "message": "Last name cannot contain leading or trailing spaces.",
            "status_code": 400,
        }

    # If none of the above conditions are met, return a success message
    return {"success": True, "message": "Input is valid.", "status_code": 200}

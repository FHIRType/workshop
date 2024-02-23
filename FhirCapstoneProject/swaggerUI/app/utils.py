import re
from datetime import datetime


test_data = {
    "Endpoint": "Humana",
    "DateRetrieved": "01-21-2024",
    "FullName": "John Smith",
    "NPI": "0112073111",
    "FirstName": "John",
    "LastName": "Smith",
    "Gender": "Male",
    "Taxonomy": "X02332D2",
    "GroupName": "Orthodontist",
    "ADD1": "1234 Johnson St.",
    "ADD2": "5678 NW Ave",
    "City": "Chicago",
    "State": "Illinois",
    "Zip": "12234",
    "Phone": "9712131232",
    "Fax": "5031231234",
    "Email": "abc@gmail.com",
    "lat": "lat_data",
    "lng": "lng_data",
    "LastPracUpdate": "LastPracUpdate_data",
    "LastPracRoleUpdate": "LastPracRoleUpdate_data",
    "LastLocationUpdate": "LastLocationUpdate_data",
    "AccuracyScore": "0.5",
}


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

    required_fields = [
        "Endpoint",
        "DateRetrieved",
        "FullName",
        "NPI",
        "FirstName",
        "LastName",
        "Gender",
        "Taxonomy",
        "GroupName",
        "ADD1",
        "City",
        "State",
        "Zip",
        "Phone",
        "Fax",
        "Email",
        "lat",
        "lng",
        "LastPracUpdate",
        "LastPracRoleUpdate",
        "LastLocationUpdate",
        "AccuracyScore",
    ]

    # Define regex patterns for specific formats
    phone_pattern = r"^\d{10}$"  # Matches 10 digits
    email_pattern = r"^\S+@\S+\.\S+$"  # Simple email pattern, can be more complex

    missing_fields = []

    # Specific constraints
    npi_length = 10

    # Check if all required fields are present and validate them
    for field in required_fields:
        # if field not in test_data:
        value = test_data.get(
            field, ""
        ).strip()  # Get the value of the field or None if not present
        if not value:
            missing_fields.append(field)

    if missing_fields:
        return {
            "success": False,
            "message": f"Missing required fields: {', '.join(missing_fields)}",
            "status_code": 400,
        }

    # Validate specific fields based on their types or constraints
    for field, value in test_data.items():
        # Date format validation
        if field == "DateRetrieved":
            try:
                datetime.strptime(value, "%m-%d-%Y")
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid date format for `{field}`. Entry must be MM-DD-YYYY.",
                    "status_code": 400,
                }

        # NPI length validation
        if field == "NPI" and len(value) != npi_length:
            return {
                "success": False,
                "message": f"NPI must be exactly {npi_length} digits.",
                "status_code": 400,
            }

        # Phone number format validation
        if field == "Phone" and not re.match(phone_pattern, value):
            return {
                "success": False,
                "message": f"Invalid phone number format for `{field}`.",
                "status_code": 400,
            }

        # Email format validation
        if field == "Email" and not re.match(email_pattern, value):
            return {
                "success": False,
                "message": f"Invalid email format for `{field}`.",
                "status_code": 400,
            }

        # Additional checks for other fields can be added here...

    # Check for logical consistency among fields (e.g., if one field is provided, another field should also be provided)
    if "ADD2" in test_data and not test_data["ADD1"]:
        return {
            "success": False,
            "message": "Address line 2 provided without Address line 1.",
            "status_code": 400,
        }

    # Add more logical consistency checks as needed...

    return {"success": True, "message": "Input is valid.", "status_code": 200}


# Test the function with the provided test data
validation_result = validate_inputs(test_data)

# Display the validation result
if validation_result["success"]:
    print("Received successfully!")
else:
    print("Error.", validation_result["message"], validation_result["status_code"])

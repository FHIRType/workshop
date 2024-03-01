import re
import unittest
import requests
from datetime import datetime

test_data = {
    "Endpoint": "Humana",
    "DateRetrieved": "01-21-2024",
    "FullName": "John Smith",
    "NPI": "0112073111",
    "FirstName": " John",
    "LastName": "Smith ",
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

fake_urls = {
    "URL": "https://www.google.com/",  # works
    "URL2": "http://localhost:8080",  # doesn't work
    "URL3": "http://unavailableserver.org",  # doesn't work
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
    npi_length = 10  # NPI length constraint

    # Check if URL field is present
    if 'URL' in test_data:
        url = test_data['URL']
        for fake_url in fake_urls.values():
            if url == fake_url:
                return {
                    "success": False,
                    "message": f"The URL endpoint {url} is not allowed.",
                    "status_code": 403
                }
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"The URL endpoint {url} is currently down.",
                    "status_code": 503
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Error connecting to URL endpoint {url}: {str(e)}",
                "status_code": 503
            }

    # Check if NPI field is present and validate its format
    npi_value = test_data.get("NPI", "")
    if not npi_value:
        return {
            "success": False,
            "message": "NPI field is missing.",
            "status_code": 400
        }

    # Validate NPI format using regular expression
    if not npi_value.isdigit():
        return {
            "success": False,
            "message": "NPI must contain only digits.",
            "status_code": 400
        }

    # Validate NPI length
    if len(npi_value) != npi_length:
        return {
            "success": False,
            "message": f"NPI must be exactly {npi_length} digits.",
            "status_code": 400
        }

    # Check FirstName field
    first_name = test_data.get("FirstName", "").strip()
    if not first_name:
        return {
            "success": False,
            "message": "First name is required.",
            "status_code": 400
        }

    # Check if FirstName has leading or trailing spaces
    if first_name != test_data["FirstName"].strip():
        return {
            "success": False,
            "message": "First name cannot contain leading or trailing spaces.",
            "status_code": 400
        }

    # Check LastName field
    last_name = test_data.get("LastName", "").strip()
    if not last_name:
        return {
            "success": False,
            "message": "Last name is required.",
            "status_code": 400
        }

    # Check if LastName has leading or trailing spaces
    if last_name != test_data["LastName"].strip():
        return {
            "success": False,
            "message": "Last name cannot contain leading or trailing spaces.",
            "status_code": 400
        }

    # If none of the above conditions are met, return a success message
    return {"success": True, "message": "Input is valid.", "status_code": 200}


# Test the function with the provided test data
validation_result = validate_inputs(test_data)

# Display the validation result
if validation_result["success"]:
    print("Received successfully!")
else:
    print("Error.", validation_result["message"], validation_result["status_code"])

class TestValidation(unittest.TestCase):
    """
    Unit tests for the validate_inputs function.
    """
    def test_fake_url_bypass(self):
        """
        Test the behavior of validate_inputs when fake URLs are provided.
        """
        for key, url in fake_urls.items():
            test_data_copy = test_data.copy()
            test_data_copy["URL"] = url

            # Perform validation
            validation_result = validate_inputs(test_data_copy)

            # Assert that the validation fails due to the fake URL
            self.assertFalse(validation_result["success"], f"URL: {url}")
            self.assertEqual(validation_result["message"], f"The URL endpoint {url} is not allowed.")
            self.assertEqual(validation_result["status_code"], 403)

    def test_valid_url(self):
        """
        Test the behavior of validate_inputs when a valid URL is provided.
        """
        # Set a valid URL
        test_data_copy = test_data.copy()
        test_data_copy["URL"] = "https://www.validurl.com"

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation succeeds
        self.assertTrue(validation_result["success"])
        self.assertEqual(validation_result["message"], "Input is valid.")
        self.assertEqual(validation_result["status_code"], 200)
    def test_unavailable_url(self):
        """
        Test the behavior of validate_inputs when an unavailable URL is provided.
        """
        # Set an unavailable URL
        test_data_copy = test_data.copy()
        test_data_copy["URL"] = "http://unavailableserver.org"

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to an unavailable URL
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "The URL endpoint http://unavailableserver.org is not allowed.")
        self.assertEqual(validation_result["status_code"], 403)

    def test_missing_npi(self):
        """
        Test the behavior of validate_inputs when the NPI field is missing.
        """
        # Remove the NPI from test data
        test_data_copy = test_data.copy()
        del test_data_copy["NPI"]

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to missing NPI
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "NPI field is missing.")
        self.assertEqual(validation_result["status_code"], 400)

    def test_invalid_npi_format(self):
        """
        Test the behavior of validate_inputs when the NPI format is invalid.
        """
        # Modify NPI to contain non-digit characters
        test_data_copy = test_data.copy()
        test_data_copy["NPI"] = "abc123"

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to invalid NPI format
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "NPI must contain only digits.")
        self.assertEqual(validation_result["status_code"], 400)

    def test_invalid_npi_length(self):
        """
        Test the behavior of validate_inputs when the NPI length is invalid.
        """
        # Modify NPI to have an invalid length
        test_data_copy = test_data.copy()
        test_data_copy["NPI"] = "123456789"

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to invalid NPI length
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "NPI must be exactly 10 digits.")
        self.assertEqual(validation_result["status_code"], 400)


if __name__ == '__main__':
    unittest.main()
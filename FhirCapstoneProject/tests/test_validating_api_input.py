import unittest
from FhirCapstoneProject.swaggerUI.app.utils import validate_inputs


class TestValidation(unittest.TestCase):
    """
    Unit tests for the validate_inputs function.
    """

    def setUp(self):
        self.test_data = {
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

    def test_missing_npi(self):
        """
        Test the behavior of validate_inputs when the NPI field is missing.
        """
        # Remove the NPI from test data
        test_data_copy = self.test_data.copy()
        del test_data_copy["NPI"]

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to missing NPI
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "NPI field is missing.")
        self.assertEqual(validation_result["status_code"], 400)

    def test_invalid_npi_length(self):
        """
        Test the behavior of validate_inputs when the NPI length is invalid.
        """
        # Modify NPI to have an invalid length
        test_data_copy = self.test_data.copy()
        test_data_copy["NPI"] = "123456789"

        # Perform validation
        validation_result = validate_inputs(test_data_copy)

        # Assert that the validation fails due to invalid NPI length
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "NPI must be exactly 10 digits.")
        self.assertEqual(validation_result["status_code"], 400)


if __name__ == "__main__":
    unittest.main()

import unittest
import requests
import validate_inputs from "./FhirCapstoneProject/swaggerUI/app/utils.py"

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

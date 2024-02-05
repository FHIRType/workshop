# Authors: Trenton Young
# Description: Tests each step of initializing a smart client to an arbitrary endpoint

import mock
import pytest
import requests


@pytest.fixture
def test_get_data_from_api_successful():
    # Mock the requests.get method to return a successful response
    with mock.patch('requests.get') as mock_get:
        # Set up a call to requests.get in the scope of this function to behave this way
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        # Use a function that will call requests.get
        result = requests.get("thing")  # Will return the mock above

        assert (result == {"key": "value"})

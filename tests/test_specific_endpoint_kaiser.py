# Authors: Iain Richey, Trenton Young
# Description: Tests the connection to Kaiser using the current configuration.

import pytest
import configparser
from fhirtypepkg.endpoint import Endpoint
from fhirtypepkg.client import SmartClient

reader = configparser.ConfigParser()

try:
    reader.read_file(open('src/fhirtypepkg/config/Endpoints.ini', 'r'))
except FileNotFoundError:
    reader.read_file(open('src/fhirtypepkg/config/server_endpoints.ini', 'r'))

sections = reader.sections()
choice = "Kaiser"
endpoint_for_testing = None
def test_create_endpoint():
    endpoint_for_testing = Endpoint(reader.get(choice, "name"), reader.get(choice, "host"),
                                    reader.get(choice, "address"), reader.getboolean(choice, "ssl"))


def test_kaiser_http_connection():
    """
    Initializes a SmartClient for this endpoint and attempts to establish an HTTP connection
    PASS: HTTP Connection is successful and the member variable .http_session_confirmed is True

    CONCERNS:
        - This is hardcoded to a single endpoint.
        - This is a long-running test.
    """
    client = SmartClient(endpoint_for_testing)

    assert client.http_session_confirmed


def test_kaiser_find_practitioner_responds():
    """
    Initializes a SmartClient for this endpoint and calls .find_practitioner on common names.
    PASS: .find_practitioner returns more than zero responses

    CONCERNS:
        - This is hardcoded to a single endpoint.
        - This is a long-running test.
        - This is a very flaky test.
    """
    client = SmartClient(endpoint_for_testing)

    assert len(client.find_practitioner("Matthew", "Smith", "")) > 0

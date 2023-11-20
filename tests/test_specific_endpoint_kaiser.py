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
    reader.read_file(open('src/fhirtypepkg/config/ServerEndpoints.ini', 'r'))

sections = reader.sections()
choice = "Kaiser"
endpoint_for_testing = None


@pytest.fixture
def create_kaiser_endpoint():
    return Endpoint(reader.get(choice, "name"), reader.get(choice, "host"),
                    reader.get(choice, "address"), reader.getboolean(choice, "ssl"))

@pytest.fixture
def smartclient_find_practitioner(create_kaiser_endpoint):
    """
    Initializes a SmartClient for this endpoint and calls .find_practitioner on common names.
    PASS: .find_practitioner returns more than zero responses

    CONCERNS:
        - This is not a unit test
        - This is hardcoded to a single endpoint.
        - This is a long-running test.
        - This is a very flaky test that relies on "Matthew Smith" being a common name for practitioners at endpoint.
    """
    client = SmartClient(create_kaiser_endpoint)
    response = client.find_practitioner("Matthew", "Smith", "")

    return response


def test_smartclient_http_connection(create_kaiser_endpoint):
    """
    Initializes a SmartClient for this endpoint and attempts to establish an HTTP connection
    PASS: HTTP Connection is successful and the member variable .http_session_confirmed is True

    CONCERNS:
        - This is (ostensibly) hardcoded to a single endpoint.
        - This is a long-running test.
    """
    client = SmartClient(create_kaiser_endpoint)

    assert client.http_session_confirmed


def test_smartclient_find_practitioner_responds(smartclient_find_practitioner):
    """
    Initializes a SmartClient for this endpoint and calls .find_practitioner on common names.
    PASS: .find_practitioner returns more than zero responses

    CONCERNS:
        - This is not a unit test
        - This is hardcoded to a single endpoint.
        - This is a long-running test.
        - This is a very flaky test that relies on "Matthew Smith" being a common name for practitioners at endpoint.
    """
    assert len(smartclient_find_practitioner) > 0


def test_smartclient_find_practitionerrole_responds(create_kaiser_endpoint, smartclient_find_practitioner):
    """
    Initializes a SmartClient for this endpoint and calls .find_practitioner_role on the first practitioner found in
    another test.
    PASS: .find_practitioner_role returns more than zero responses

    CONCERNS:
        - This is not a unit test
        - This is hardcoded to a single endpoint.
        - This is a long-running test.
        - This is a very flaky test that relies on the result of another test having associated roles.
    """
    client = SmartClient(create_kaiser_endpoint)
    response = client.find_practitioner_role(smartclient_find_practitioner[0])

    assert len(response) > 0


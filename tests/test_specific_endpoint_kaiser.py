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
endpoint_kaiser = Endpoint(reader.get(choice, "name"), reader.get(choice, "host"), reader.get(choice, "address"), reader.getboolean(choice, "ssl"))


def test_kaiser_http_connection():
    client = SmartClient(endpoint_kaiser)

    assert client.http_session_confirmed


def test_kaiser_get_practitioner_responds():
    client = SmartClient(endpoint_kaiser)

    assert len(client.find_practitioner("Matthew", "Smith", "")) > 0

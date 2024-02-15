# Authors: Iain Richey, Trenton Young
# Description: Tests the static functions of the SmartClient namespace.

import pytest
import configparser

import FhirCapstoneProject.fhirtypepkg.client as ClientNamespace

from requests import Request
import fhirclient.models.practitioner as Practitioner

from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.client import SmartClient


@pytest.fixture
def create_http_enabled_endpoint():
    return Endpoint(
        "Name",
        "hostname",
        "address",
        True,
    )


@pytest.fixture
def create_search_parameters():
    return {
        "boolean_true": True,
        "boolean_false": False,
        "int": 1,
        "string": "string",
    }


@pytest.fixture
def create_test_endpoint_without_ssl():
    return Endpoint(
        "Test Endpoint",
        "host.name",
        "/address/",
        False,
        False,
        False
    )


@pytest.fixture
def create_test_smart_client_without_ssl(create_test_endpoint_without_ssl):
    return SmartClient(create_test_endpoint_without_ssl)


def test_endpoint_url_of_smart_client(create_test_smart_client_without_ssl):
    assert create_test_smart_client_without_ssl.get_endpoint_url() == "http://host.name/address/"


def test_endpoint_name_of_smart_client(create_test_smart_client_without_ssl):
    assert create_test_smart_client_without_ssl.get_endpoint_name() == "Test Endpoint"


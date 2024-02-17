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


def test_http_build_search(create_search_parameters):
    """
    Tests the basic usage of http_build_search with bools, integers,
    and strings
    by checking that the params generated from a Request match those supplied to the http_build_search function.
    """
    output = ClientNamespace.http_build_search(create_search_parameters)

    request = Request(params=output)
    result_values = request.params

    assert result_values[0][0] == "boolean_true"
    assert result_values[0][1] == create_search_parameters["boolean_true"]

    assert result_values[1][0] == "boolean_false"
    assert result_values[1][1] == create_search_parameters["boolean_false"]

    assert result_values[2][0] == "int"
    assert result_values[2][1] == create_search_parameters["int"]

    assert result_values[3][0] == "string"
    assert result_values[3][1] == create_search_parameters["string"]


def test_fhir_build_search(create_search_parameters):
    """
    Tests the basic usage of fhir_build_search with bools, integers,
    and strings
    by checking that the params generated from a Request match those supplied to the http_build_search function.
    """
    arbitrary_resource = Practitioner.Practitioner
    output = ClientNamespace.fhir_build_search(
        arbitrary_resource, create_search_parameters
    )

    for param in output.params:
        assert create_search_parameters[param.name] == param.value

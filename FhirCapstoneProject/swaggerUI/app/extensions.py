import configparser
import os

import asyncio
from flask_restx import Api

from FhirCapstoneProject.fhirtypepkg import fhirtype
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.model.accuracy import calc_accuracy
from FhirCapstoneProject.model.analysis import predict
from FhirCapstoneProject.model.match import group_rec

import json
from FhirCapstoneProject.fhirtypepkg.smartclient import SmartClient

# Parse Endpoints configuration file
script_dir = os.path.dirname(os.path.abspath(__file__))

endpoint_config_dir = os.path.join(
    script_dir, "..", "..", "fhirtypepkg", "config/ServerEndpoints.ini"
)
endpoint_config_path = str(endpoint_config_dir)

try:
    assert os.path.isfile(endpoint_config_path)
except AssertionError as e:
    print(
        f"ERROR: Logging Configuration file doesn't exist at {endpoint_config_path}. ",
        e,
    )

endpoint_config_parser = configparser.ConfigParser()
endpoint_config_parser.read_file(open(endpoint_config_path, "r"))
endpoint_configs = endpoint_config_parser.sections()

endpoints = []
for (
    section
) in (
    endpoint_configs
):  # loop through each endpoint in our config and initialize it as an endpoint in a usable array
    try:
        endpoints.append(
            Endpoint(
                name=endpoint_config_parser.get(section, "name"),
                host=endpoint_config_parser.get(section, "host"),
                address=endpoint_config_parser.get(section, "address"),
                enable_http=endpoint_config_parser.getboolean(
                    section, "enable_http", fallback=False
                ),
                use_http_client=endpoint_config_parser.getboolean(
                    section, "use_http_client", fallback=False
                ),
                get_metadata_on_init=endpoint_config_parser.get(
                    section, "get_metadata_on_init", fallback=False
                ),
                can_search_by_npi=endpoint_config_parser.getboolean(
                    section, "can_search_by_npi", fallback=False
                ),
                secure_connection_needed=endpoint_config_parser.getboolean(
                    section, "ssl", fallback=False
                ),
                id_prefix=endpoint_config_parser.get(
                    section, "id_prefix", fallback=None
                ),
            )
        )
    except ValueError as e:
        print(f"Error processing section {section}: {e}")

# Initialize an empty dictionary to store SmartClient objects for each endpoint
smart_clients = {}


def init_smart_client(endpoint: Endpoint):
    smart_clients[endpoint.name] = SmartClient(endpoint)


def init_all_smart_clients():
    # Instantiate each endpoint as a Smart Client
    for endpoint in endpoints:
        init_smart_client(endpoint)

    fhirtype.fhir_logger().info("*** CONNECTION ESTABLISHED TO ALL ENDPOINTS ***")


init_all_smart_clients()


def get_endpoint_names():
    return [endpoint.name for endpoint in endpoints]


api = Api(version="0.0", title="FHIR API", description="FHIR API from PacificSource")


def search_practitioner(
    family_name: str, given_name: str, npi: str or None, resolve_references=True
):
    """
    Searches for a practitioner based on the given name, family name, and NPI.

    Parameters:
    family_name: The family name of the practitioner.
    given_name: The given name of the practitioner.
    npi: The NPI of the practitioner.

    Returns:
    A tuple containing a list of all matching practitioners and the predicted best match.
    """
    responses, flattened_responses = [], []

    for client_name, client in smart_clients.items():
        print("PRAC: CLIENT NAME IS ", client_name)
        practitioners, flattened_data = asyncio.run(client.find_practitioner(
                family_name, given_name, npi, resolve_references
            )
        )

        if practitioners is not None:
            responses.extend(practitioners)

        if flattened_data is not None:
            flattened_responses.extend(flattened_data)

    return responses, flattened_responses if responses else None


def search_practitioner_role(
    family_name: str, given_name: str, npi: str or None, resolve_references=False
):
    """
    :param resolve_references:
    :param family_name:
    :param given_name:
    :param npi:
    :return:
    """
    # A list of practitioners returned from external endpoints
    all_results, _ = search_practitioner(
        family_name=family_name,
        given_name=given_name,
        npi=npi,
        resolve_references=resolve_references,
    )
    responses = []
    flatten_data = []
    for client_name, client in smart_clients.items():
        print("ROLE: CLIENT NAME IS ", client_name)
        for response in all_results:
            role, _flatten_data = client.find_practitioner_role(
                response, resolve_references=resolve_references
            )

            if not role or not _flatten_data:
                continue

            responses.extend(role)
            flatten_data.extend(_flatten_data)

    return responses, flatten_data if responses else None


def search_location(family_name: str, given_name: str, npi: str or None):
    all_results, _ = search_practitioner_role(
        family_name=family_name, given_name=given_name, npi=npi, resolve_references=True
    )

    responses = []
    flatten_data = []
    for client_name in smart_clients:
        print("LOC: CLIENT NAME IS ", client_name)
        client = smart_clients[client_name]

        for role in all_results:
            # Continue if the client is wrong
            if role.origin_server.base_uri != client.endpoint.get_url():
                continue

            location, flat = client.find_practitioner_role_locations(role)

            responses.extend(location)
            flatten_data.extend(flat)

    return responses, flatten_data if responses else None


async def search_all_practitioner_data(
    family_name: str,
    given_name: str,
    npi: str or None,
    endpoint: str or None = None,
    consensus: bool = False,
):
    flatten_data = []

    # unspecified endpoint
    if endpoint is None:
        for client_name in smart_clients:
            print("ALL: CLIENT NAME IS ", client_name)
            client = smart_clients[client_name]
            client.init_flatten_class()
            flat_data = await client.find_all_practitioner_data(family_name, given_name, npi)
            flatten_data.extend(flat_data)
    else:  # specified endpoint
        if endpoint in smart_clients:
            print("SPECIFIC: CLIENT NAME IS ", endpoint)
            client = smart_clients[endpoint]
            client.init_flatten_class()
            flat_data = await client.find_all_practitioner_data(family_name, given_name, npi)
            flatten_data.extend(flat_data)
        else:
            print(f"Warning: Endpoint '{endpoint}' not found among clients.")

    if consensus:
        predicted = predict(flatten_data)
        consensus_data = calc_accuracy(flatten_data, predicted)
        consensus_data.append(predicted)

        return consensus_data

    return flatten_data


def match_data(collection: list):
    matched_practitioner = group_rec(collection)

    return matched_practitioner


def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data
    that is in JSON format but needs to be converted first
    """

    if resource is not None:
        for index, res in enumerate(resource):
            print("Result ", index + 1)
            print(json.dumps(res.as_json(), sort_keys=False, indent=2))
            print("\n\n")

        print("Total results: ", len(resource))

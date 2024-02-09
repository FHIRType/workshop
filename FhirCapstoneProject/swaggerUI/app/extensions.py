from flask_restx import Api

import configparser
from FhirCapstoneProject.fhirtypepkg import fhirtype
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.client import SmartClient


# Parse Endpoints configuration file
endpoint_config_parser = configparser.ConfigParser()
endpoint_config_parser.read_file(open("FhirCapstoneProject/fhirtypepkg/config/ServerEndpoints.ini", "r"))
endpoint_configs = endpoint_config_parser.sections()

endpoints = []
for (
        section
) in (
        endpoint_configs
):  # loop through each endpoint in our config and initialize it as a endpoint in a usable array
    try:
        endpoints.append(
            Endpoint(
                name=endpoint_config_parser.get(section, "name"),
                host=endpoint_config_parser.get(section, "host"),
                address=endpoint_config_parser.get(section, "address"),
                enable_http=endpoint_config_parser.getboolean(
                    section, "enable_http", fallback=False
                ),
                get_metadata_on_init=endpoint_config_parser.getboolean(
                    section, "get_metadata_on_init", fallback=False
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

    fhirtype.fhir_logger().info(
        "*** CONNECTION ESTABLISHED TO ALL ENDPOINTS ***"
    )

init_all_smart_clients()


api = Api(version='0.0', title='FHIR API',
          description='FHIR API from PacificSource')


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
    responses = []

    for client_name, client in smart_clients.items():
        print("PRAC: CLIENT NAME IS ", client_name)
        practitioners, flattened_data = client.find_practitioner(
            family_name, given_name, npi, resolve_references
        )

        if not practitioners:
            continue

        responses.extend(practitioners)

    return responses, flattened_data if responses else None

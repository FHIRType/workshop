# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import configparser
import json
import os

import asyncio

import psycopg2

from datetime import date

from dotenv import load_dotenv

import FhirCapstoneProject.fhirtypepkg.fhirtype
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.client import SmartClient
from FhirCapstoneProject.fhirtypepkg.queryhelper import QueryHelper
from FhirCapstoneProject.fhirtypepkg.analysis import predict


# Parse Endpoints configuration file
endpoint_config_parser = configparser.ConfigParser()
endpoint_config_parser.read_file(open("src/fhirtypepkg/config/Endpoints.ini", "r"))
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

# TODO: Put test data in a flat file, read that

# Load envrionment variables (.env)
load_dotenv()

try:
    # Connect to the database server (local)
    local_postgres_db = psycopg2.connect(
        database=os.getenv("DATABASE"),
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
    )

    local_query_helper = QueryHelper(connector=local_postgres_db)

    # Sample data
    data = {
        "version_id": "907",
        "last_updated": str(date(2023, 11, 22)),
        "active": "True",
        "gender": "Female",
    }

    # insert sample data to our database server (local)
    local_query_helper.insert(type="practitioner", data=data)

    print(local_query_helper.fetch_all("practitioner"))
except psycopg2.OperationalError:
    pass


def print_all(all_results, predicted=None, flat_data=None, temp=1):
    if all_results:
        print(f"\n\nAll results ({len(all_results)})")
        print_resource(all_results)
        if flat_data is not None:
            print(f"\n\nFlattened ({len(flat_data)} endpoints)")
            if temp == 1:
                for data in flat_data:
                    print_res_obj(data)
            elif temp == 2:
                for datas in flat_data:
                    for data in datas:
                        print_res_obj(data)
    else:
        print("\nNo matching results :(")
        print("\nHence, no predicted result as well:(\n\n")


def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    if resource is not None:
        for index, res in enumerate(resource):
            print("Result ", index + 1)
            print(json.dumps(res.as_json(), sort_keys=False, indent=2))
            print("\n\n")


def print_res_obj(dict_obj):
    """
    Prints the keys and values of a dictionary in a formatted manner.

    This function iterates over each key-value pair in the input dictionary,
    and prints them in the format: "key : value". After printing all pairs,
    it prints a newline for better readability.

    Parameters:
    :param dict_obj: The dictionary to print.
    :type dict_obj: dict
    """
    for res in dict_obj:
        print(res, ": ", dict_obj[res])
    print("\n")


def dict_has_all_keys(check: dict, keys: list[str]):
    missing = 0
    for key in keys:
        if key not in check.keys():
            missing += 1

    return missing == 0


async def init_smart_client(endpoint: Endpoint):
    smart_clients[endpoint.name] = SmartClient(endpoint)


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
    flattened_dataS = []
    predicted_response = None

    for client_name, client in smart_clients.items():
        print("CLIENT NAME IS ", client_name)
        practitioners, filtered_data = client.find_practitioner(
            family_name, given_name, npi, resolve_references
        )

        if not practitioners or not filtered_data:
            continue

        responses.extend(practitioners)
        flattened_dataS.extend(filtered_data)

    return responses, [predicted_response], flattened_dataS if responses else None


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
    all_results, _ , _ = search_practitioner(
        family_name=family_name,
        given_name=given_name,
        npi=npi,
        resolve_references=resolve_references,
    )
    responses = []
    consensus_data = []
    predicted_role = None

    for client_name, client in smart_clients.items():
        print("CLIENT NAME IS ", client_name)
        for response in all_results:
            role, filtered_dict = client.find_practitioner_role(
                response, resolve_references=resolve_references
            )

            if role and filtered_dict:
                responses.extend(role)
                consensus_data.append(filtered_dict)

    return responses, [predicted_role], consensus_data if responses else None


def search_location(family_name: str, given_name: str, npi: str or None):
    all_results, _, _ = search_practitioner_role(
        family_name=family_name, given_name=given_name, npi=npi, resolve_references=True
    )

    responses = []
    consensus_data = []
    predicted_location = None
    for client_name in smart_clients:
        print("CLIENT NAME IS ", client_name)
        client = smart_clients[client_name]

        for role in all_results:
            # Continue if the client is wrong
            if role.origin_server.base_uri != client.endpoint.get_url():
                continue

            location, filtered_dict = client.find_practitioner_role_locations(role)

            if not location or not filtered_dict:
                continue

            responses.extend(location)
            consensus_data.extend(filtered_dict)

    return responses, [predicted_location], consensus_data if responses else None


def search_organization(family_name: str, given_name: str, npi: str or None):
    all_results, predicted = search_practitioner_role(
        family_name=family_name, given_name=given_name, npi=npi, resolve_references=True
    )
    responses = []
    consensus_data = []

    for client_name in smart_clients:
        print("CLIENT NAME IS ", client_name)
        client = smart_clients[client_name]
        for role in all_results:
            if role.origin_server.base_uri != client.endpoint.get_url():
                continue

            organization, filtered_dict = client.find_practitioner_role_organization(
                role
            )

            if not organization or not filtered_dict:
                continue

            responses.extend(organization)
            consensus_data.extend(filtered_dict)

        predicted_org_id, predicted_org = (
            predict(consensus_data) if consensus_data else (None, None)
        )

        if predicted_org_id is not None:
            for res in responses:
                if res.id == predicted_org_id:
                    predicted_org = res
                    break

    return responses, [predicted_org] if responses else None


async def main():
    # Instantiate each endpoint as a Smart Client
    connection_schedule = []

    for endpoint in endpoints:
        connection_schedule.append(init_smart_client(endpoint))

    await asyncio.gather(*connection_schedule)

    FhirCapstoneProject.fhirtypepkg.fhirtype.fhir_logger().info(
        "*** CONNECTION ESTABLISHED TO ALL ENDPOINTS ***"
    )

    ##########################################
    # INTERACTIVE MODE
    ##########################################
    ##########################################

    run = True
    cmd_history = []
    curr_cmd = ""

    # PROMPT
    ##########################################

    while run:
        curr_cmd = input(": ")
        cmd_history.append(curr_cmd)

        handled_cmd = curr_cmd.split(" ")

        cmd = handled_cmd[0].lower()
        if cmd == "exit":
            run = False
        elif cmd == "test":
            if len(handled_cmd) == 1:
                print("Test function")
            else:
                print("Test function was passed args: ", handled_cmd[1:])
        elif cmd == "get":
            if len(handled_cmd) != 2:
                print("ERROR Usage: get resource?param=arg")
                continue

            try:
                resource, query = handled_cmd[1].split("?")
                resource, query = resource.lower(), query.lower()
                params = {}
                for pair in query.split("&"):
                    param, arg = pair.split("=")
                    params[param] = arg
            except ValueError:
                print("ERROR Usage: get resource?param=arg")
                continue

            if resource == "practitioner":
                all_results, predicted, flat_response = search_practitioner(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_all(all_results, predicted, flat_response, 1)

            elif resource == "practitionerrole":
                all_results, predicted, flat_response = search_practitioner_role(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_all(all_results, predicted, flat_response, 2)

            elif resource == "location":
                all_results, predicted, flat_response = search_location(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_all(all_results, predicted, flat_response)

            elif resource == "organization":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    all_results, predicted = search_organization(
                        params["family_name"], params["given_name"], params["npi"]
                    )
                    # print_all(all_results, predicted)
                    print_resource(all_results)

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_organization(
                        params["family_name"], params["given_name"], None
                    )
                    # print_all(all_results, predicted)
                    print_resource(all_results)
                else:
                    print(
                        "ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))"
                    )
                    continue

            else:
                print(f"ERROR Usage: unknown resource type '{resource}'")

        else:
            print(f"command '{cmd}' not recognized")


if __name__ == "__main__":
    asyncio.run(main())

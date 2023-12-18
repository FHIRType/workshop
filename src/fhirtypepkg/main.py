# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import configparser
import json
import os

import asyncio

# import psycopg2

from datetime import date

# from dotenv import load_dotenv
from fhirclient.models.capabilitystatement import CapabilityStatement

import src.fhirtypepkg.fhirtype
from src.fhirtypepkg.endpoint import Endpoint
from src.fhirtypepkg.client import SmartClient
from src.fhirtypepkg.queryhelper import QueryHelper
from src.fhirtypepkg.standardize import standardize_practitioner_data
from src.fhirtypepkg.standardize import StandardizedResource
from src.fhirtypepkg.analysis import predict


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
    endpoints.append(
        Endpoint(
            name=endpoint_config_parser.get(section, "name"),
            host=endpoint_config_parser.get(section, "host"),
            address=endpoint_config_parser.get(section, "address"),
            secure_connection_needed=endpoint_config_parser.getboolean(section, "ssl"),
            id_prefix=endpoint_config_parser.get(section, "id_prefix", fallback=None),
        )
    )

# Initialize an empty dictionary to store SmartClient objects for each endpoint
smart_clients = {}

# TODO: Put test data in a flat file, read that

# # Load envrionment variables (.env)
# load_dotenv()
#
# # Connect to the database server (local)
# local_postgres_db = psycopg2.connect(
#     database=os.getenv("DATABASE"),
#     host=os.getenv("HOST"),
#     user=os.getenv("USER"),
#     password=os.getenv("PASSWORD"),
#     port=os.getenv("PORT"),
# )
#
# local_query_helper = QueryHelper(connector=local_postgres_db)
#
# # Sample data
# data = {
#     "version_id": "907",
#     "last_updated": str(date(2023, 11, 22)),
#     "active": "True",
#     "gender": "Female",
# }
#
# # insert sample data to our database server (local)
# local_query_helper.insert(type="practitioner", data=data)
#
# print(local_query_helper.fetch_all("practitioner"))


def print_all(all_results, predicted):
    if all_results and predicted:
        print("\n\nAll results")
        print_resource(all_results)
        print("\n\nPredicted Result")
        print_resource(predicted)
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


def search_practitioner(family_name: str, given_name: str, npi: str or None):
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
    consensus_data = []

    for client_name, client in smart_clients.items():
        print("CLIENT NAME IS ", client_name)
        practitioners, filtered_data = client.find_practitioner(family_name, given_name, npi)

        if not practitioners or not filtered_data:
            continue

        responses.extend(practitioners)
        consensus_data.extend(filtered_data)

    predicted_prac_id, predicted_prac = (
        predict(consensus_data) if consensus_data else (None, None)
    )

    if predicted_prac_id is not None:
        for res in responses:
            if res.id == predicted_prac_id:
                predicted_prac = res
                break

    return responses, [predicted_prac] if responses else None


def search_practitioner_role(family_name: str, given_name: str, npi: str or None):
    """
    :param family_name:
    :param given_name:
    :param npi:
    :return:
    """
    # A list of practitioners returned from external endpoints
    all_results, predicted_practitioner = search_practitioner(
        family_name=family_name, given_name=given_name, npi=npi
    )
    responses = []
    consensus_data = []
    for client_name, client in smart_clients.items():
        print("CLIENT NAME IS ", client_name)
        for response in all_results:
            role, filtered_dict = client.find_practitioner_role(response)

            if not role or not filtered_dict:
                continue

            responses.extend(role)
            consensus_data.extend(filtered_dict)

    predicted_role_id, predicted_role = (
        predict(consensus_data) if consensus_data else (None, None)
    )

    if predicted_role_id is not None:
        for res in responses:
            if res.id == predicted_role_id:
                predicted_role = res
                break

    return responses, [predicted_role] if responses else None


def search_location(family_name: str, given_name: str, npi: str or None):
    all_results, predicted = search_practitioner_role(
        family_name=family_name, given_name=given_name, npi=npi
    )

    responses = []
    consensus_data = []
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

        predicted_loc_id, predicted_loc = (
            predict(consensus_data) if consensus_data else (None, None)
        )

        if predicted_loc_id is not None:
            for res in responses:
                if res.id == predicted_loc_id:
                    predicted_loc = res
                    break

    return responses, [predicted_loc] if responses else None


def search_organization(family_name: str, given_name: str, npi: str or None):
    all_results, predicted = search_practitioner_role(
        family_name=family_name, given_name=given_name, npi=npi
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

    src.fhirtypepkg.fhirtype.fhir_logger().info(
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
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    all_results, predicted = search_practitioner(
                        params["family_name"], params["given_name"], params["npi"]
                    )
                    print_all(all_results, predicted)

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_practitioner(
                        params["family_name"], params["given_name"], None
                    )
                    print_all(all_results, predicted)

                else:
                    print(
                        "ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))"
                    )
                    continue

            elif resource == "practitionerrole":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    all_results, predicted = search_practitioner_role(
                        params["family_name"], params["given_name"], params["npi"]
                    )
                    print_all(all_results, predicted)

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_practitioner_role(
                        params["family_name"], params["given_name"], None
                    )
                    print_all(all_results, predicted)

                else:
                    print(
                        "ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))"
                    )
                    continue

            elif resource == "location":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    all_results, predicted = search_location(
                        params["family_name"], params["given_name"], params["npi"]
                    )
                    print_all(all_results, predicted)

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_location(
                        params["family_name"], params["given_name"], None
                    )
                    print_all(all_results, predicted)

                else:
                    print(
                        "ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))"
                    )
                    continue

            elif resource == "organization":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    all_results, predicted = search_organization(
                        params["family_name"], params["given_name"], params["npi"]
                    )
                    print_all(all_results, predicted)

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_organization(
                        params["family_name"], params["given_name"], None
                    )
                    print_all(all_results, predicted)

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

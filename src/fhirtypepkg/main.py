# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import configparser
import json
import os

import asyncio
#import psycopg2

from datetime import date
#from dotenv import load_dotenv
from fhirclient.models.capabilitystatement import CapabilityStatement

import fhirtypepkg.fhirtype
from fhirtypepkg.endpoint import Endpoint
from fhirtypepkg.client import SmartClient
from fhirtypepkg.queryhelper import QueryHelper
from fhirtypepkg.standardize import standardize_practitioner_data
from fhirtypepkg.standardize import StandardizedResource
from fhirtypepkg.analysis import predict


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
            endpoint_config_parser.get(section, "name"),
            endpoint_config_parser.get(section, "host"),
            endpoint_config_parser.get(section, "address"),
            endpoint_config_parser.getboolean(section, "ssl"),
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
    print("\n\nAll results")
    print_resource(all_results)
    print("\n\nPredicted Result")
    print_resource(predicted)

def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    if resource is not None:
        for index, res in enumerate(resource):
            print("Result ", index+1)
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
        print(f"Querying client: {client_name}")
        practitioners, filtered_data = client.find_practitioner(given_name, family_name, npi)

        if not practitioners or not filtered_data:
            continue

        responses.extend(practitioners)
        consensus_data.extend(filtered_data)

    predicted_prac_id, predicted_prac = predict(consensus_data) if consensus_data else (None, None)

    if predicted_prac_id is not None:
        for res in responses:
            if res.id == predicted_prac_id:
                predicted_prac = res
                break

    return responses, [predicted_prac] if responses else None

def search_practitioner_role(family_name: str, given_name: str, npi: str or None):
    """
    TODO: These functions will need to do a lot of concurrent processing to be any kind of reasonable
    :param family_name:
    :param given_name:
    :param npi:
    :return:
    """
    # A list of practitioners returned from external endpoints
    all_results , predicted_practitioner = search_practitioner(family_name=family_name, given_name=given_name, npi=npi)
    responses = []
    consensus_data = []
    for client_name, client in smart_clients.items():
        for response in all_results:
            role, filtered_dict = client.find_practitioner_role(response)

            if not role or not filtered_dict:
                continue

            responses.extend(role)
            consensus_data.extend(filtered_dict)

    predicted_role_id, predicted_role = predict(consensus_data) if consensus_data else (None, None)

    if predicted_role_id is not None:
        for res in responses:
            if res.id == predicted_role_id:
                predicted_role = res
                break

    return responses, [predicted_role] if responses else None

    # TODO: Database needs to serve up endpoints and practitioner ID from this NPI that we can find roles for

    # practRow: https://kpx.org/prac/533uo499452, https://cigna....,

    # resources.append(queryHelper.getPractitioner(family_name, given_name, npi))

    # TODO: If the database didn't return anything,
    #  OR if we decide that we also want to include "thorough"
    #  flag or something like that,
    #  we can perform as search on the SmartClients as well to get data from them (not just the database)

    # for resource in resources:
    #     # TODO: Need to be able to trace back to the source of the data, associating a PK with that endpoint
    #     #  Resources, thus, must contain some reference to their source.
    #     #  This can just be the URL it was retrieved from
    #     #  as that contains both the API endpoint and its identifier on that platform.

    #     # get endpoint by url from resource
    #     data_source = resource["data_source"]  # TODO: Localization

    #     client = fhirtypepkg.fhirtype.get_by_url(smart_clients, data_source)

    #     resources.append(client.find_pracititioner_role(resource["identifier"]))  # TODO: Localization

    # consensus = predict(responses)

    # queryHelper.insert(consensus)

    # return consensus
    # return [
    #     {"role_thing": "PLACEHOLDEER", "role_name": "PLACEHOLDRO"}  # TODO: Localization
    # ]
    # if len(responses) > 0:
    #     return responses[0]
    # else:
    #     return None


def search_location(family_name: str, given_name: str, npi: str or None):
    all_results, predicted = search_practitioner_role(family_name=family_name, given_name=given_name, npi=npi)

    responses = []
    consensus_data = []
    for client_name in smart_clients:
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

    return responses


def search_organization(family_name: str, given_name: str, npi: str or None):
    resources = search_practitioner_role(family_name=family_name, given_name=given_name, npi=npi)

    responses = []
    for client_name in smart_clients:
        client = smart_clients[client_name]
        for res in resources:
            response = client.find_practitioner_role_organization(res)

            if len(response[0]) > 0 and len(response[1]) > 0:
                responses.append(response[0])

    return responses


async def main():

    # Instantiate each endpoint as a Smart Client
    connection_schedule = []

    for endpoint in endpoints:
        connection_schedule.append(init_smart_client(endpoint))

    await asyncio.gather(*connection_schedule)

    fhirtypepkg.fhirtype.fhir_logger().info("*** CONNECTION ESTABLISHED TO ALL ENDPOINTS ***")

    ##########################################
    # INTERACTIVE MODE
    ##########################################
    ##########################################

    run = True
    cmd_history = []
    curr_cmd = ""

    # GET Practitioner?given_name=this&family_name=that
    # GET Practitioner?given_name=this&family_name=that&npi=1000000000
    # GET PractitionerRole?given_name=this&family_name=that
    # GET PractitionerRole?given_name=this&family_name=that&npi=1000000000
    # GET Location?given_name=this&family_name=that
    # GET Location?given_name=this&family_name=that&npi=1000000000
    # GET Organization?given_name=this&family_name=that
    # GET Organization?given_name=this&family_name=that&npi=1000000000

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
                    print_resource(search_practitioner(params["family_name"], params["given_name"], params["npi"]))

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_practitioner(params["family_name"], params["given_name"], None)
                    print_all(all_results, predicted)

                else:
                    print("ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))")
                    continue

            elif resource == "practitionerrole":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    print_resource(search_practitioner_role(params["family_name"], params["given_name"], params["npi"]))

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    all_results, predicted = search_practitioner_role(params["family_name"], params["given_name"], None)
                    print_all(all_results, predicted)

                else:
                    print("ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))")
                    continue

            elif resource == "location":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    print_resource(search_location(params["family_name"], params["given_name"], params["npi"]))

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    print_resource(search_location(params["family_name"], params["given_name"], None))

                else:
                    print("ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))")
                    continue

            elif resource == "organization":
                if dict_has_all_keys(params, ["family_name", "given_name", "npi"]):
                    print_resource(search_organization(params["family_name"], params["given_name"], params["npi"]))

                elif dict_has_all_keys(params, ["family_name", "given_name"]):
                    print_resource(search_organization(params["family_name"], params["given_name"], None))

                else:
                    print("ERROR Usage: expected params (given_name, family_name, npi) OR (given_name, family_name))")
                    continue

            else:
                print(f"ERROR Usage: unknown resource type '{resource}'")

        else:
            print(f"command '{cmd}' not recognized")

    #
    #
    # for client in smart_clients:
    #     # Print the name of the endpoint for the current SmartClient
    #     print("\n  ####  ", smart_clients[client].get_endpoint_name(), "  ####")
    #
    #     # Loop through each data item in provider_lookup_name_data
    #     for data in provider_lookup_name_data:
    #         # Use the SmartClient to find practitioners that match the data
    #         resources, filtered_dict = smart_clients[client].find_practitioner(
    #             data["f_name"], data["l_name"], data["NPI"]
    #         )
    #
    #         # If any practitioners were found...
    #         if resources:
    #             print("\nProvider Data\n")
    #             for resource in resources:
    #                 # Print the standardized data for the practitioner
    #                 for filtered in filtered_dict:
    #                     print_res_obj(filtered)
    #
    #                 # Find and print the roles for the practitioner
    #                 roles, filtered_dict = smart_clients[client].find_practitioner_role(
    #                     resource
    #                 )
    #                 if roles:
    #                     print("\nPractitioner Role Data\n")
    #                     for role in roles:
    #                         print_res_obj(filtered_dict)
    #
    #                         # Find and print the locations for the role
    #                         locations, filtered_dict = smart_clients[
    #                             client
    #                         ].find_practitioner_role_locations(role)
    #                         if locations:
    #                             print("\nLocation Data\n")
    #                             for filtered in filtered_dict:
    #                                 print_res_obj(filtered)
    #
    #                         # Find and print the organizations for the role
    #                         organizations, filtered_dict = smart_clients[
    #                             client
    #                         ].find_practitioner_role_organization(role)
    #                         if organizations:
    #                             print("\nOrganization Data\n")
    #                             for organization in organizations:
    #                                 print_res_obj(filtered_dict)
    #
    #         # If no practitioners were found, print "..."
    #         else:
    #             print("...", end="")


if __name__ == "__main__":
    asyncio.run(main())

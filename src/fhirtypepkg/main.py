# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import configparser
import json
import os

import asyncio
import psycopg2

from datetime import date
from dotenv import load_dotenv
from fhirclient.models.capabilitystatement import CapabilityStatement

from fhirtypepkg.endpoint import Endpoint
from fhirtypepkg.client import SmartClient
from fhirtypepkg.queryhelper import QueryHelper
from fhirtypepkg.standardize import standardize_practitioner_data
from fhirtypepkg.standardize import StandardizedResource


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


def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    print(json.dumps(resource.as_json(), sort_keys=False, indent=2))


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


async def init_smart_client(endpoint: Endpoint):
    smart_clients[endpoint.name] = SmartClient(endpoint)


def search_practitioner(family_name: str, given_name: str, npi: str):
    responses = []
    for client in smart_clients:
        responses.append(client.find_practitioner(given_name, family_name, npi))

    # consensus = predict(responses)

    # queryHelper.insert(consensus)

    # return consensus
    return [
        {"given_name": "Doctor", "family_name": "Beer"}
    ]


def main():

    # Instantiate each endpoint as a Smart Client
    # for endpoint in endpoints:
    #      asyncio.run(init_smart_client(endpoint))

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

# Practitioner?name=this&age=that
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
                print(search_practitioner(params["family_name"], params["given_name"], params["npi"]))
            elif resource == "practitionerrole":
                print("Finding a practitionerrole")
            elif resource == "location":
                print("Finding a location")
            elif resource == "organization":
                print("Finding an organization")
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
    main()

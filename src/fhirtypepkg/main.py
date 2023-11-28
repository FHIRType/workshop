# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import json
import configparser

# import postgresql
# from postgresql import driver
from endpoint import Endpoint
from client import SmartClient
import psycopg2
import os
# from persistent.queryhelper import QueryHelper
from dotenv import load_dotenv
from standardize import standardize_practitioner_data
from standardize import StandardizedResource

from fhirclient.models.capabilitystatement import CapabilityStatement

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


provider_lookup_name_data = [
    {
        "f_name": "Brandon",
        "l_name": "Bianchini",
        "NPI": "1700158326",
        "prac_resp": "None",
        "prac_role_resp": "None",
        "loc_resp": "None",
    },
    {
        "f_name": "Kaydie",
        "l_name": "Satein",
        "NPI": "1619302171",
        "prac_resp": "None",
        "prac_role_resp": "None",
        "loc_resp": "None",
    },
    # {"f_name": "Toren", "l_name": "Davis", "NPI": "1457779498", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "Marilyn", "l_name": "Darr", "NPI": "1902844418", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "David", "l_name": "Ruiz", "NPI": "1508803982", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "Olivia", "l_name": "Wright", "NPI": "1205876182", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "John", "l_name": "Nusser", "NPI": "1467549204", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    {
        "f_name": "Melinda",
        "l_name": "Landchild",
        "NPI": "1992743546",
        "prac_resp": "None",
        "prac_role_resp": "None",
        "loc_resp": "None",
    },
    # {"f_name": "Natasha", "l_name": "Ingvoldstad-O'Neal", "NPI": "1689871147", "prac_resp": "None",
    #  "prac_role_resp": "None", "loc_resp": "None"},
    # {"f_name": "Michael", "l_name": "Liu", "NPI": "1841210549", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "David", "l_name": "Paik", "NPI": "1023218047", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "Adriana", "l_name": "Linares", "NPI": "1558577130", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"}
]

# Load envrionment variables (.env)
load_dotenv()

# Connect to the database server (local)
conn = psycopg2.connect(database=os.getenv("DATABASE"),
                        host=os.getenv("HOST"),
                        user=os.getenv("USER"),
                        password=os.getenv("PASSWORD"),
                        port=os.getenv("PORT"))

print(conn)

def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    print(json.dumps(resource.as_json(), sort_keys=False, indent=2))


def print_res_obj(obj):
    for res in obj:
        print(res, ": ", obj[res])
    print("\n")


def main():
    # TODO: Initialize these concurrently, the requests should all be sent at the same time - perhaps use asyncio? (iain)
    smart_clients = {}
    for endpoint in endpoints:
        smart_clients[endpoint.name] = SmartClient(endpoint)

    for client in smart_clients:
        print("\n  ####  ", smart_clients[client].get_endpoint_name(), "  ####")

        for data in provider_lookup_name_data:
            resources, filtered_dict = smart_clients[client].find_practitioner(
                data["f_name"], data["l_name"], data["NPI"]
            )

            if resources:
                print("\nProvider Data\n")
                for resource in resources:
                    # print_resource(resource)
                    print_res_obj(filtered_dict)
                    # Standardized = StandardizedResource(resource)
                    # print_resource(resource)
                    # print_res_obj(filtered_dict)

                    roles, filtered_dict = smart_clients[client].find_practitioner_role(
                        resource
                    )
                    if roles:
                        print("\nPractitioner Role Data\n")
                        for role in roles:
                            # Standardized.setPractitionerRole(role)
                            print_res_obj(filtered_dict)
                            # print_resource(role)

                            locations, filtered_dict = smart_clients[
                                client
                            ].find_practitioner_role_locations(role)
                            if locations:
                                print("\nLocation Data\n")
                                # for location in locations:
                                for fil in filtered_dict:
                                    # print_resource(location)
                                    print_res_obj(fil)
                                    # Standardized.setLocation(location)
                                    # print_res_obj(Standardized.LOCATION.filtered_dictionary)
                                    # print_resource(Standardized.RESOURCE)

                            organizations, filtered_dict = smart_clients[
                                client
                            ].find_practitioner_role_organization(role)
                            if organizations:
                                print("\nOrganization Data\n")
                                for organization in organizations:
                                    print_res_obj(filtered_dict)
                                    # Standardized.setOrganization(organization)
                                    # print_res_obj(Standardized.ORGANIZATION.filtered_dictionary)
                                    # print_resource(Standardized.RESOURCE)

            else:
                print("...", end="")


if __name__ == "__main__":
    main()

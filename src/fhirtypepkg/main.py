# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import json
import configparser
# import postgresql
# from postgresql import driver
from endpoint import Endpoint
from client import SmartClient
from standardize import standardize_data

from fhirclient.models.capabilitystatement import CapabilityStatement

# Parse Endpoints configuration file
endpoint_config_parser = configparser.ConfigParser()
endpoint_config_parser.read_file(open('src/fhirtypepkg/config/Endpoints.ini', 'r'))
endpoint_configs = endpoint_config_parser.sections()

endpoints = []
for section in endpoint_configs: #loop through each endpoint in our config and initialize it as a endpoint in a usable array
    endpoints.append(Endpoint(endpoint_config_parser.get(section, "name"), endpoint_config_parser.get(section, "host"), endpoint_config_parser.get(section, "address"), endpoint_config_parser.getboolean(section, "ssl")))


# Parse LocalDatabase configuration file
# local_database_config_parser = configparser.ConfigParser()
# local_database_config_parser.read_file(open('src/fhirtypepkg/config/LocalDatabase.ini', 'r'))

# postgreSQL_config = {
#     "user": local_database_config_parser.get("PostgreSQL", "user"),
#     "password": local_database_config_parser.get("PostgreSQL", "password"),
#     "host": local_database_config_parser.get("PostgreSQL", "host"),
#     "port": local_database_config_parser.get("PostgreSQL", "port"),
#     "database": local_database_config_parser.get("PostgreSQL", "database"),
# }


# Connect to LocalDatabase with config info
# local_db = postgresql.driver.connect(
#     user=postgreSQL_config['user'],
#     password=postgreSQL_config['password'],
#     host=postgreSQL_config['host'],
#     port=postgreSQL_config['port'],
#     database=postgreSQL_config['database'],
# )

# db_test = local_db.prepare("SELECT * FROM practitioner;")
# print(db_test())

provider_lookup_name_data = [
    # {"f_name": "Brandon", "l_name": "Bianchini", "NPI": "1700158326", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    {"f_name": "Kaydie", "l_name": "Satein", "NPI": "1619302171", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Toren", "l_name": "Davis", "NPI": "1457779498", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Marilyn", "l_name": "Darr", "NPI": "1902844418", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "David", "l_name": "Ruiz", "NPI": "1508803982", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Olivia", "l_name": "Wright", "NPI": "1205876182", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "John", "l_name": "Nusser", "NPI": "1467549204", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Melinda", "l_name": "Landchild", "NPI": "1992743546", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Natasha", "l_name": "Ingvoldstad-O'Neal", "NPI": "1689871147", "prac_resp": "None",
     "prac_role_resp": "None", "loc_resp": "None"},
    # {"f_name": "Michael", "l_name": "Liu", "NPI": "1841210549", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "David", "l_name": "Paik", "NPI": "1023218047", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "Adriana", "l_name": "Linares", "NPI": "1558577130", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"}
]


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
        # endpoint.print_info()
        smart_clients[endpoint.name] = SmartClient(endpoint)


    # print(len(smart_clients["Kaiser"].find_practitioner("Matthew", "Smith", "")) > 0)

    # for _client in clients:
    #     req = "metadata"
    #     query = "GET " + _client.get_endpoint_url() + req
    #     print(query, _client.http_query(req), sep=" | ")

    for client in smart_clients:
        print("\n  ####  ", smart_clients[client].get_endpoint_name(), "  ####")
        print("\nProvider Data\n")
        for data in provider_lookup_name_data:
            resources = smart_clients[client].find_practitioner(data["f_name"], data["l_name"], data["NPI"])

            resource = None
            roles = []
            locations = []
            organizations = []

            if resources and len(resources) > 0:
                print_res_obj(standardize_data(resources[0]))
                resource = resources[0]

                roles = smart_clients[client].find_practitioner_role(resource)

                if roles:
                    for role in roles:
                        locations.append(smart_clients[client].find_practitioner_role_locations(role))
                        organizations.append(smart_clients[client].find_practitioner_role_organization(role))


            # if resource:
            #     # print_resource(resource)
            #     if smart_clients[client].get_endpoint_name() == "Humana":
            #         print_res_obj(getHumanaData(resource))
            #     elif smart_clients[client].get_endpoint_name() == "Kaiser":
            #         print_res_obj(getKaiserData(resource))
            else:
                print("...", end="")


if __name__ == "__main__":
    main()


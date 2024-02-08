# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import configparser
import json
import asyncio
from FhirCapstoneProject.fhirtypepkg import fhirtype
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.client import SmartClient
from FhirCapstoneProject.fhirtypepkg.analysis import predict


# TODO: Need to get all these globals and such into a class to be called. These can cause issues in other modules.
#  Ideally no file IO or HTTP action would happen without the user specifically calling it because it may would happen without

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

        print("Total results: ", len(resource))


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

    for client_name, client in smart_clients.items():
        print("PRAC: CLIENT NAME IS ", client_name)
        practitioners, flattened_data = client.find_practitioner(
            family_name, given_name, npi, resolve_references
        )

        if not practitioners:
            continue

        responses.extend(practitioners)

    return responses, flattened_data if responses else None


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
        print("CLIENT NAME IS ", client_name)
        client = smart_clients[client_name]

        for role in all_results:
            # Continue if the client is wrong
            if role.origin_server.base_uri != client.endpoint.get_url():
                continue

            location, flat_data = client.find_practitioner_role_locations(role)

            if not location or not flat_data:
                continue

            responses.extend(location)
            flatten_data.extend(flat_data)

    return responses, flatten_data if responses else None


async def main():
    # Instantiate each endpoint as a Smart Client
    connection_schedule = []

    for endpoint in endpoints:
        connection_schedule.append(init_smart_client(endpoint))

    await asyncio.gather(*connection_schedule)

    fhirtype.fhir_logger().info(
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
                all_results, flatten_data = search_practitioner(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_resource(all_results)
                print(flatten_data)

            elif resource == "practitionerrole":
                all_results, flatten_data = search_practitioner_role(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_resource(all_results)
                pretty_printed_json = json.dumps(flatten_data, indent=4)
                print(pretty_printed_json)

            elif resource == "location":
                all_results = search_location(
                    params["family_name"], params["given_name"], params["npi"]
                )
                print_resource(all_results)

            else:
                print(f"ERROR Usage: unknown resource type '{resource}'")

        else:
            print(f"command '{cmd}' not recognized")


if __name__ == "__main__":
    asyncio.run(main())

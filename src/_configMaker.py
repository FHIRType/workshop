# Authors: Iain Richey, Trenton Young
# Description: Creates the config files needed by our program

import os
import configparser
import sys

#List of API endpoints
endpoints = [
    {'name': 'Humana', 'host': 'fhir.humana.com', 'address': '/sandbox/api/', 'ssl': 'True'},
    {'name': 'Kaiser', 'host': 'kpx-service-bus.kp.org', 'address': '/service/hp/mhpo/healthplanproviderv1rc/', 'ssl': 'True'},
    {'name': 'Cigna', 'host': 'p-hi2.digitaledge.cigna.com', 'address': '/ProviderDirectory/v1/', 'ssl': 'True'},
    {'name': 'Centene', 'host': 'production.api.centene.com', 'address': '/fhir/providerdirectory/', 'ssl': 'False'},
    {'name': 'Pacificsource', 'host': 'api.apim.pacificsource.com', 'address': '/fhir/provider/R4/', 'ssl': 'True'}
]

def endpoint_configurator(filename: str):
    target = f'src/fhirtypepkg/config/{filename}.ini'

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Loop through our endpoints
    for endpoint in endpoints:
        # Add a section for that endpoint
        config_parser.add_section(endpoint.get("name"))

        # Add its corresponding data
        config_parser.set(endpoint.get("name"), "name", endpoint.get("name"))
        config_parser.set(endpoint.get("name"), "host", endpoint.get("host"))
        config_parser.set(endpoint.get("name"), "address", endpoint.get("address"))
        config_parser.set(endpoint.get("name"), "ssl", endpoint.get("ssl"))

    with open(target, 'w+') as configfile:
        config_parser.write(configfile)


def database_configurator_blank(filename: str):
    target = f'src/fhirtypepkg/config/{filename}.ini'

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Add a section for that endpoint
    config_parser.add_section("PostgreSQL")

    # Add its corresponding data
    config_parser.set("PostgreSQL", "user", "None")
    config_parser.set("PostgreSQL", "password", "None")
    config_parser.set("PostgreSQL", "host", "None")
    config_parser.set("PostgreSQL", "port", "None")
    config_parser.set("PostgreSQL", "database", "None")

    with open(target, 'w+') as configfile:
        config_parser.write(configfile)


def main():
    """
    Generates configuration files for use with the FHIRType application.

    -endpoints <NAME> :: Generate a config file for Endpoints and store as a .ini file named NAME
    -database-blank <NAME> :: Generate a blank config file for a local PostgreSQL Database and store as a .ini file
    named NAME
    """
    args = sys.argv[1:]

    if args[0] == "--help":
        print("Generates configuration files for use with the FHIRType application.\n\n"
              "-endpoints <NAME> :: Generate a config file for Endpoints and store as a .ini file named NAME\n"
              "-database-blank <NAME> :: Generate a blank config file for a local PostgreSQL Database and store as"
              " a .ini file named NAME\n", sep=" ")
    else:
        for i in range(0, len(args), 2):
            flag = args[i]
            value = args[i + 1]

            if flag == "-endpoints":
                endpoint_configurator(value)

            if flag == "-database-blank":
                database_configurator_blank(value)


if __name__ == "__main__":
    main()

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
    # {'name': 'Pacificsource', 'host': 'api.apim.pacificsource.com', 'address': '/fhir/provider/R4/', 'ssl': 'True'}
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


def logger_configurator_default(filename: str):
    target = f'src/fhirtypepkg/config/{filename}.ini'

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Sections and options
    config_parser.add_section("loggers")
    config_parser.set("loggers", "keys", "root,FHIR")

    config_parser.add_section("handlers")
    config_parser.set("handlers", "keys", "consoleHandler")

    config_parser.add_section("formatters")
    config_parser.set("formatters", "keys", "simpleFormatter")

    config_parser.add_section("logger_root")
    config_parser.set("logger_root", "level", "DEBUG")
    config_parser.set("logger_root", "handlers", "consoleHandler")

    config_parser.add_section("logger_FHIR")
    config_parser.set("logger_FHIR", "level", "DEBUG")
    config_parser.set("logger_FHIR", "handlers", "consoleHandler")
    config_parser.set("logger_FHIR", "qualname", "FHIR")
    config_parser.set("logger_FHIR", "propagate", "0")

    config_parser.add_section("handler_consoleHandler")
    config_parser.set("handler_consoleHandler", "class", "StreamHandler")
    config_parser.set("handler_consoleHandler", "level", "DEBUG")
    config_parser.set("handler_consoleHandler", "formatter", "simpleFormatter")
    config_parser.set("handler_consoleHandler", "args", "(sys.stdout,)")

    config_parser.add_section("formatter_simpleFormatter")
    config_parser.set("formatter_simpleFormatter", "format", "%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s")
    config_parser.set("formatter_simpleFormatter", "datefmt", "%Y-%m-%d %I:%M:%S %p")

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
              "-database-blank <NAME> :: Generate a blank config file for a local PostgreSQL Database and store as\n"
              "-logger <NAME> :: Generate a default config file for the logger"
              " a .ini file named NAME\n", sep=" ")
    else:
        for i in range(0, len(args), 2):
            flag = args[i]
            value = args[i + 1]

            if flag == "-endpoints":
                endpoint_configurator(value)

            if flag == "-database-blank":
                database_configurator_blank(value)

            if flag == "-logger":
                logger_configurator_default(value)


if __name__ == "__main__":
    main()

# Authors: Iain Richey, Trenton Young
# Description: Creates the config files needed by our program
import json
import os
import configparser
import sys

# List of API endpoints
# default_endpoints = [
#     {
#         "name": "Humana",
#         "host": "fhir.humana.com",
#         "address": "/sandbox/api/",
#         "ssl": "True",
#     },
#     {
#         "name": "Kaiser",
#         "host": "kpx-service-bus.kp.org",
#         "address": "/service/hp/mhpo/healthplanproviderv1rc/",
#         "ssl": "True",
#     },
#     {
#         "name": "Cigna",
#         "host": "p-hi2.digitaledge.cigna.com",
#         "address": "/ProviderDirectory/v1/",
#         "ssl": "True",
#     },
#     {
#         "name": "Centene",
#         "host": "production.api.centene.com",
#         "address": "/fhir/providerdirectory/",
#         "ssl": "False",
#     },
# ]
#
# with open("src/fhirtypepkg/config/default_endpoints.txt", "w+") as f:
#     json.dump(default_endpoints, f, indent=None)


def endpoint_configurator(filename: str, endpoints: list):
    target = f"src/fhirtypepkg/config/{filename}.ini"

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

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def database_configurator_blank(filename: str):
    target = f"src/fhirtypepkg/config/{filename}.ini"

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

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def logger_configurator_default(filename: str):
    target = f"src/fhirtypepkg/config/{filename}.ini"

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
    config_parser.set(
        "formatter_simpleFormatter",
        "format",
        "%(asctime)s: %(filename)s %(levelname)s - %(lineno)d %(message)s",
    )
    config_parser.set("formatter_simpleFormatter", "datefmt", "%Y-%m-%d %I:%M:%S %p")

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def main():
    """
    Generates configuration files for use with the FHIRType application.

    Options - include any number of these options and follow them with arguments. Some options may take `.` as
    an argument to enter interactive mode.

    -endpoints <NAME> <blank | . | "[file.json]" >
        Generate a config file for Endpoints and store as a .ini file named NAME in the `config` directory. If
        the arg given is 'blank', a default meaningless config file will be generated that has helpful
        placeholder values in it. A `.` arg will enter interactive mode. A json arg will generate a config file
        using that data.
    -database-blank <NAME>.
        Generate a blank config file for a local PostgreSQL Database and store as a .ini file named NAME in
        the `config` directory
    """
    args = sys.argv[1:]

    if len(args) < 1 or args[0] == "--help":
        print(main.__doc__)
    else:
        i = 0
        while i < len(args):
            flag = args[i]
            i += 1

            filename = args[i]
            i += 1

            value = args[i]
            i += 1

            ##########################################
            # Handle generating endpoint config files
            ##########################################
            if flag == "-endpoints":
                # Interactive Mode
                if value == ".":
                    # TODO: Need to actually implement interactive mode
                    print("INTERACTIVE MODE")

                # Template generator
                elif value == "blank":
                    endpoint_configurator(filename, [{
                        "name": "BLANK",
                        "host": "SUB.DOMAIN.com",
                        "address": "/FHIR/",
                        "ssl": "True"}
                    ])

                # JSON parser
                else:
                    with open(value) as fi:
                        endpoint_configurator(filename, json.load(fi))

            ##########################################
            # Handle generating database connection config files
            ##########################################
            if flag == "-database-blank":
                database_configurator_blank(filename)

            ##########################################
            # Handle generating logger config files
            ##########################################
            if flag == "-logger":
                logger_configurator_default(filename)


if __name__ == "__main__":
    main()

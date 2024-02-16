# Authors: Iain Richey, Trenton Young, Hla Htun
# Description: Creates the config files needed by our program
import json
import configparser
import sys

from FhirCapstoneProject.fhirtypepkg.fhirtype import fhir_logger


def endpoint_configurator(filename: str, endpoints: list):
    target = f"src/fhirtypepkg/config/{filename}.ini"

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Loop through our endpoints
    for endpoint in endpoints:
        try:
            # Add a section for that endpoint
            config_parser.add_section(endpoint.get("name"))

            # Add its corresponding data
            config_parser.set(endpoint.get("name"), "name", str(endpoint.get("name")))
            config_parser.set(endpoint.get("name"), "host", str(endpoint.get("host")))
            config_parser.set(
                endpoint.get("name"), "address", str(endpoint.get("address"))
            )
            config_parser.set(endpoint.get("name"), "ssl", str(endpoint.get("ssl")))
            config_parser.set(
                endpoint.get("name"),
                "enable_http",
                str(endpoint.get("enable_http", False)),
            )
            config_parser.set(
                endpoint.get("name"),
                "get_metadata_on_init",
                str(endpoint.get("get_metadata_on_init", False)),
            )

        except TypeError as e:
            fhir_logger().error(
                "ERROR While making config files, check that your endpoint "
                'source has all required options. (Failed while parsing endpoint: "%s")',
                str(endpoint.get("name", "NO NAME PROVIDED")),
            )
            raise e

        # Add optional data
        if "id_prefix" in endpoint.keys():
            config_parser.set(
                str(endpoint.get("name")), "id_prefix", str(endpoint.get("id_prefix"))
            )

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def database_configurator(filename: str, configuration: dict):
    target = f"src/fhirtypepkg/config/{filename}.ini"

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Add a section for that endpoint
    config_parser.add_section("PostgreSQL")

    # Add its corresponding data
    config_parser.set("PostgreSQL", "user", configuration.get("user"))
    config_parser.set("PostgreSQL", "password", configuration.get("password"))
    config_parser.set("PostgreSQL", "host", configuration.get("host"))
    config_parser.set("PostgreSQL", "port", configuration.get("port"))
    config_parser.set("PostgreSQL", "database", configuration.get("database"))

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def logger_configurator_default(filename: str):
    target = f"src/fhirtypepkg/config/{filename}.ini"

    # Create a configParser object
    config_parser = configparser.RawConfigParser()

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
    -database <NAME> <blank | . | "[file.json]" >
        Generate a config file for a local PostgreSQL server and store as a .ini file named NAME in the `config`
        directory. If the arg given is 'blank', a default meaningless config file will be generated that has helpful
        placeholder values in it. A `.` arg will enter interactive mode. A json arg will generate a config file
        using that data.
    -logger <NAME> <blank>
        Generate a config file for a FHIR logger, MUST use the blank keyword at this time.
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
                    print("TODO INTERACTIVE MODE")

                # Template generator
                elif value == "blank":
                    endpoint_configurator(
                        filename,
                        [
                            {
                                "name": "BLANK",
                                "host": "SUB.DOMAIN.com",
                                "address": "/FHIR/",
                                "ssl": "True",
                            }
                        ],
                    )

                # JSON parser
                else:
                    with open(value) as fi:
                        endpoint_configurator(filename, json.load(fi))

            ##########################################
            # Handle generating database connection config files
            ##########################################
            if flag == "-database":
                # Interactive Mode
                if value == ".":
                    # TODO: Need to actually implement interactive mode
                    print("TODO INTERACTIVE MODE")

                # Template generator
                elif value == "blank":
                    database_configurator(
                        filename,
                        {
                            "user": "BLANK",
                            "password": "BLANK",
                            "host": "BLANK",
                            "port": "BLANK",
                            "database": "BLANK",
                        },
                    )

                # JSON parser
                else:
                    with open(value) as fi:
                        database_configurator(filename, json.load(fi))

            ##########################################
            # Handle generating logger config files
            ##########################################
            if flag == "-logger":
                logger_configurator_default(filename)


if __name__ == "__main__":
    main()

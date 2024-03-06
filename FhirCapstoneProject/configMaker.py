# Authors: Iain Richey, Trenton Young, Hla Htun
# Description: Creates the config files needed by our program
import configparser
import json
import os
import sys
import typer


def endpoint_configurator(filename: str, endpoints: list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(script_dir, f"fhirtypepkg/config/{filename}.ini")
    target = str(target_dir)

    # Create a configParser object
    config_parser = configparser.ConfigParser()

    # Loop through our endpoints
    for _endpoint in endpoints:
        try:
            # Add a section for that endpoint
            config_parser.add_section(_endpoint.get("name"))

            # Add its corresponding data
            config_parser.set(_endpoint.get("name"), "name", str(_endpoint.get("name")))
            config_parser.set(_endpoint.get("name"), "host", str(_endpoint.get("host")))
            config_parser.set(
                _endpoint.get("name"), "address", str(_endpoint.get("address"))
            )
            config_parser.set(_endpoint.get("name"), "ssl", str(_endpoint.get("ssl")))
            config_parser.set(
                _endpoint.get("name"),
                "enable_http",
                str(_endpoint.get("enable_http", False)),
            )
            config_parser.set(
                _endpoint.get("name"),
                "use_http_client",
                str(_endpoint.get("use_http_client", False)),
            )
            config_parser.set(
                _endpoint.get("name"),
                "get_metadata_on_init",
                str(_endpoint.get("get_metadata_on_init", False)),
            )

        except TypeError as e:
            print(
                "ERROR While making config files, check that your endpoint "
                'source has all required options. (Failed while parsing endpoint: "%s")',
                str(_endpoint.get("name", "NO NAME PROVIDED")),
                file=sys.stderr,
            )
            raise e

        # Add optional data
        if "id_prefix" in _endpoint.keys():
            config_parser.set(
                str(_endpoint.get("name")), "id_prefix", str(_endpoint.get("id_prefix"))
            )

    with open(target, "w+") as configfile:
        config_parser.write(configfile)


def database_configurator(filename: str, configuration: dict):
    target = f"FhirCapstoneProject/fhirtypepkg/config/{filename}.ini"

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
    target = f"FhirCapstoneProject/fhirtypepkg/config/{filename}.ini"

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


app = typer.Typer()


@app.command()
def endpoint(config_file: str, src: str = None):
    """
    Generate a config file for Endpoints and store as a .ini file in the `config` directory.

    :param config_file: Destination name which the config will be written to (in the config directory)

    :param src: A JSON file path, or if blank a default meaningless config file will be generated that has helpful
    placeholder values in it.
    """
    if src is None:
        endpoint_configurator(
            config_file,
            [
                {
                    "name": "BLANK",
                    "host": "SUB.DOMAIN.com",
                    "address": "/FHIR/",
                    "ssl": "True",
                }
            ],
        )
    else:
        with open(src) as fi:
            endpoint_configurator(config_file, json.load(fi))


@app.command()
def database(config_file: str, src: str = None):
    """
    Generate a config file for Database connection and store as a .ini file in the `config` directory.

    :param config_file: Destination name which the config will be written to (in the config directory)

    :param src: A JSON file path, or if blank a default meaningless config file will be generated that has helpful
    placeholder values in it.
    """
    if src is None:
        database_configurator(
            config_file,
            {
                "user": "BLANK",
                "password": "BLANK",
                "host": "BLANK",
                "port": "BLANK",
                "database": "BLANK",
            },
        )
    else:
        with open(src) as fi:
            database_configurator(config_file, json.load(fi))


@app.command()
def logging(config_file: str):
    """
    Generate a config file for the logger and store as a .ini file in the `config` directory. This command is trivial,
    because the logger takes only one default (hardcoded) configuration

    :param config_file: Destination name which the config will be written to (in the config directory)
    """
    logger_configurator_default(config_file)


if __name__ == "__main__":
    app()

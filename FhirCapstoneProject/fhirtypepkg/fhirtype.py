# Credentials and helper module  # TODO: Should be seperated out, credentials should be represented in the DB
import os
from email.message import Message
from .logging_fhir import FHIRLogger
from logging import Logger

_CONTENTTYPE_APPLICATION_JSON = "application/json"
_CONTENTTYPE_APPLICATION_FHIRJSON = "application/fhir+json"

# TODO: need to get rid of this magic string unless it will never change. These types of actions at the top of a file
# are best refactored into a class as class member or class method.
# Globals can cause a lot of headaches if there is a bug as they can span across multiple sources.
logger_config_path = "FhirCapstoneProject/fhirtypepkg/config/ServerLogging.ini"

try:
    assert os.path.isfile(logger_config_path)
except AssertionError as e:
    print(
        f"ERROR: Logging Configuration file doesn't exist at {logger_config_path}. ", e
    )

_logger = FHIRLogger(logger_config_path)


def fhir_logger() -> Logger:
    return _logger.logger


def get_app_id():
    return "test"


def get_by_url(smart_clients: dict, url: str):
    """
    Selects the first SmartClient from a dict of SmartClients that matches the URL given EXACTLY.
    :param smart_clients: A dict of SmartClient instances
    :param url: The fully qualified URL of the endpoint to be considered
    :return: None if no such endpoint is found, or the SmartClient corresponding to that URL
    """
    for client in smart_clients:
        if client.get_endpoint_url() == url:
            return client
    return None


class ExceptionNPI(Exception):
    pass


def parse_content_type_header(content_types: str) -> tuple[str, dict[str, str]]:
    """
    Credit to Philip Couling at https://stackoverflow.com/a/75727619
    This function will parse a content-type string into a usable tuple of type and options
    :param content_types: e.g. 'application/json; charset=utf-8'
    :return:
    """
    email = Message()
    email["content-type"] = content_types
    params = email.get_params()

    return params[0][0], dict(params[1:])


def content_type_is(parsed_content_type: tuple[str, dict[str, str]], _is: str):
    return parsed_content_type[0] == _is


def content_type_is_json(parsed_content_type: tuple[str, dict[str, str]]):
    return content_type_is(
        parsed_content_type, _CONTENTTYPE_APPLICATION_JSON
    ) or content_type_is(parsed_content_type, _CONTENTTYPE_APPLICATION_FHIRJSON)

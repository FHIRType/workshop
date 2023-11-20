# Credentials and helper module  # TODO: Should be seperated out, credentials should be represented in the DB
import os
from email.message import Message
from logs.logging_fhir import FHIRLogger

_CONTENTTYPE_APPLICATION_JSON = "application/json"
_CONTENTTYPE_APPLICATION_FHIRJSON = "application/fhir+json"


_logger = FHIRLogger("src/fhirtypepkg/config/Logging.ini")


def logger() -> FHIRLogger:
    return _logger.logger


def get_app_id():
    return "test"


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
    return (content_type_is(parsed_content_type, _CONTENTTYPE_APPLICATION_JSON) or
            content_type_is(parsed_content_type, _CONTENTTYPE_APPLICATION_FHIRJSON))

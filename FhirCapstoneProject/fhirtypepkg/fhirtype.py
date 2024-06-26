import os
from email.message import Message
from logging import Logger

from .logging_fhir import FHIRLogger

_CONTENTTYPE_APPLICATION_JSON = "application/json"
_CONTENTTYPE_APPLICATION_FHIRJSON = "application/fhir+json"

script_dir = os.path.dirname(os.path.abspath(__file__))
logging_dir = os.path.join(script_dir, "config", "ServerLogging.ini")
logger_config_path = str(logging_dir)

try:
    assert os.path.isfile(logger_config_path)
except AssertionError as e:
    print(
        f"ERROR: Logging Configuration file doesn't exist at {logger_config_path}. ", e
    )

_logger = FHIRLogger(logger_config_path)


def decorate_if(_f=None, decorator=None, condition=False):
    if _f is not None:
        return _f
    else:

        def inner_wrapper(f):
            if condition:
                return decorator(f)
            else:
                return f

        return inner_wrapper


def a_test_decorator(f):
    pass
    return f


@decorate_if(decorator=a_test_decorator, condition=True)
def a_test_function():
    pass


def fhir_logger() -> Logger:
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
    return content_type_is(
        parsed_content_type, _CONTENTTYPE_APPLICATION_JSON
    ) or content_type_is(parsed_content_type, _CONTENTTYPE_APPLICATION_FHIRJSON)

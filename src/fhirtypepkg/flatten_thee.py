# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re
from typing import List, Tuple, Dict, Any

from fhirclient.models.fhirreference import FHIRReference

from fhirtypepkg.fhirtype import ExceptionNPI
from fhirclient.models.domainresource import DomainResource
from fhirtypepkg.keys import *
from datetime import datetime

def is_valid_taxonomy(taxonomy: str) -> bool:
    """
    Checks if the given taxonomy is valid.

    A valid taxonomy must start with 3 digits, followed by a single letter, followed by 5 digits, and ending with the character "X".
    For example, a valid taxonomy could be "100Q00000X".

    Parameters:
    :param taxonomy: The taxonomy to validate.
    :type taxonomy: str

    Returns:
    :return: True if the taxonomy is valid, False otherwise.
    :rtype: bool
    """
    pattern = re.compile(r"^\d{3}[A-Za-z]{1}\d{5}X$")
    return bool(pattern.match(taxonomy))


def is_valid_license(license_number: str) -> bool:
    """
    Checks if the given license number is valid.

    A valid license number must start with 2 letters, followed by 5 to 12 digits.
    For example, a valid license number could be "MD61069302".

    Note: This function has only been tested with Washington licenses.

    Parameters:
    :param license_number: The license number to validate.
    :type license_number: str

    Returns:
    :return: True if the license number is valid, False otherwise.
    :rtype: bool
    """
    pattern = re.compile(r"^[A-Za-z]{2}\d{5,12}$")
    return bool(pattern.match(license_number))


def is_valid_provider_number(provider_number: str) -> bool:
    """
    Checks if the given provider number is valid.

    A valid provider number must start with 4 letters, followed by a hyphen, followed by 3 letters, another hyphen, and ending with 10 digits.
    For example, a valid provider number could be "ABCD-EFG-0000123123".

    Parameters:
    :param provider_number: The provider number to validate.
    :type provider_number: str

    Returns:
    :return: True if the provider number is valid, False otherwise.
    :rtype: bool
    """
    pattern = re.compile(r"^[A-Za-z]{4}-[A-Za-z]{3}-\d{10}$")
    return bool(pattern.match(provider_number))


def validate_npi(npi: str) -> str:
    """
    Validates that a given string may be a National Provider Identifier (NPI).

    This is a simple format test and does NOT check against any databases.
    The function will raise an ExceptionNPI if the NPI is invalid, and always returns a valid NPI.

    Parameters:
    :param npi: The NPI to validate.
    :type npi: str

    Returns:
    :return: A valid NPI of the form "0000000000".
    :rtype: str

    Raises:
    :raises ExceptionNPI: If the NPI is invalid.
    """
    m = re.match(r"([0-9]{10})", npi)

    if m is None:
        raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")
    else:
        valid_npi = m.group(0)

    if valid_npi is None:
        raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")

    return m.group(0)


def standardize_phone_number(phone_number: str) -> str:
    """
    Standardizes the given phone number.

    This function removes all non-digit characters from the phone number and adds the country code "+1" at the beginning.

    Note: Assumes all numbers are in the U.S.

    Parameters:
    :param phone_number: The phone number to standardize.
    :type phone_number: str

    Returns:
    :return: The standardized phone number.
    :rtype: str
    """
    # Remove non-digit characters
    digits_only = re.sub(r"\D", "", phone_number)
    # Add the country code
    formatted_number = (
            "+1" + digits_only
    )  # TODO: This works for now, but when we go international...

    return formatted_number


def standardize_name(name: str) -> str:
    """
    Standardizes the given name.

    This function removes all underscore characters from the name and replaces them with spaces.

    Parameters:
    :param name: The name to standardize.
    :type name: str

    Returns:
    :return: The standardized name.
    :rtype: str
    """
    # Remove "_" and replace with " ", empty spaces
    removed_underscores = re.sub(r"_", " ", name)
    return removed_underscores


def normalize(value: str, value_type: str) -> str:
    """
    Normalizes the given value based on its type.

    Currently, this function only supports the "qualification" type, for which it removes leading and trailing commas.

    Parameters:
    :param value: The value to normalize.
    :type value: str
    :param value_type: The type of the value.
    :type value_type: str

    Returns:
    :return: The normalized value.
    :rtype: str
    """
    if value_type == "qualification":
        return value.strip(", ")

    # more datatype can be specified here if needed in future


def getFullName(resource: DomainResource):
    # Will need to check which client type it is and get data accordingly
    None


def flatten_resource(resource: DomainResource, client: str):
    return {
        KEY_ENDPOINT: client,
        KEY_Data_Retrieved: datetime.utcnow(),
        KEY_FULLNAME: getFullName(),
    }, resource


class FlattenResource:
    """
    A class used to represent a Standardized Resource.

    """

    def __init__(self):
        """
        Initializes a new instance of the StandardizedResource class.
        """
        self.DATA       = None
        self.RESOURCE   = None

    def flattenResource(self, resource: DomainResource, client_name: str):
        """
        Standardizes the given practitioner resource and sets the PRACTITIONER attribute.

        Parameters:
        :param client_name:
        :param resource: The resource to standardize.
        :type resource: DomainResource
        """
        self.DATA, self.RESOURCE = flatten_resource(resource, client_name)
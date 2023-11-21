# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re
from typing import List, Tuple

from fhirclient.models.domainresource import DomainResource

from fhirtypepkg.client import validate_npi


def is_valid_taxonomy(taxonomy: str) -> bool:
    """
    Must start with 3 digits number followed by one-character letter
    Followed by 5 digits before ending with "X" character
    e.g. 207Q00000X
    """
    pattern = re.compile(r'^\d{3}[A-Za-z]{1}\d{5}X$')
    return bool(pattern.match(taxonomy))


def is_valid_license(license_number: str) -> bool:
    """
    The first two characters should be letters
    The last 5 to 12 characters must be digits
    e.g. MD61069302

    TODO: Only tested with Washington licenses
    """
    pattern = re.compile(r'^[A-Za-z]{2}\d{5,12}$')
    return bool(pattern.match(license_number))


def is_valid_kaiser_provider_number(provider_number: str) -> bool:
    """
    The first four characters and the following three characters must be letters
    The last 10 characters must be digit
    e.g. EPDM-IND-0000149013
    """
    pattern = re.compile(r'^[A-Za-z]{4}-[A-Za-z]{3}-\d{10}$')
    return bool(pattern.match(provider_number))


def normalize(value: str, value_type: str) -> str:
    """
    :param value: value is the input string to be normalized
    :param value_type: is the type of data the string is supposed to be
    :return: the normalized string
    """
    if value_type == "qualification":
        return value.strip(", ")

    # TODO: more datatype can be specified here if needed in future


def standardize_licenses(qualifications: DomainResource) -> List[str]:
    """
    Fetches all the license numbers and validates them
    :param qualifications: Qualification Domain Resource from FHIR endpoint
    :return: Every license found
    """
    licenses = []

    for qualification in qualifications:
        license_details = {}
        if qualification.extension:
            for extension in qualification.extension:
                if extension.valueCodeableConcept:
                    license_details["state"] = extension.valueCodeableConcept.coding[0].display

        if qualification.identifier:
            license_valid = is_valid_license(qualification.identifier[0].value)
            if license_valid:
                license_details["license"] = qualification.identifier[0].value
            else:
                license_details["license"] = "INVALID LICENSE NUMBER"

        if qualification.period:
            period = {
                qualification.period.start.isostring,
                qualification.period.end.isostring
            }
            license_details["period"] = period

        # only append if not empty
        if license_details:
            licenses.append(license_details)

    if licenses:
        return licenses
    else:
        return None


def standardize_qualifications(qualifications: DomainResource) -> dict:
    """
    Fetches all the important qualification data and validates them
    :param qualifications: Qualification Domain Resource from FHIR endpoint
    :return: All valid qualification information such as taxonomy and display text
    """
    # taxonomy, display = standardize_taxonomy(qualifications)
    taxonomy, display = None, None

    for qualification in qualifications:
        if qualification.code.coding:
            value = str(qualification.code.coding[0].code)
            value = value if is_valid_taxonomy(value) else None
            display = qualification.code.coding[0].display

    qualifications = {
        "taxonomy": value,
        "display": display,
    }

    return qualifications


def standardize_name(resource: DomainResource) -> dict:
    """
    Fetches the practitioner name and normalizes them
    :param resource: Domain Resource from FHIR endpoint
    :param endpoint: Specifies from which endpoint data is being queried from
    :return: The name and other details of the practitioner in standardized format
    """
    first_name, middle_name, last_name, qualification, prefix, full_name = None, None, None, None, None, None

    if resource.name:
        if resource.name[0].given[0]:
            first_name = resource.name[0].given[0]
            text = first_name.split()
            first_name = text[0]
            if len(text) >= 2:
                middle_name = text[1]

        if resource.name[0].family:
            last_name = resource.name[0].family
            last_name = last_name.split()[0]

        if resource.name[0].prefix:
            prefix = resource.name[0].prefix[0]

        if resource.name[0].text:
            text = resource.name[0].text
            if len(text) >= 5:
                full_name = resource.name[0].text
            elif len(text) < 5:
                qualification = normalize(resource.name[0].text, "qualification")

    else:
        return None

    return {"first_name": first_name, "middle_name": middle_name, "last_name": last_name, "prefix": prefix,
            "full_name": full_name, "qualification": qualification}


def standardize_identifier(identifier: DomainResource) -> dict:
    """
    Fetches all the important identifier information and validates them
    :param identifier: Identifier Domain Resource from FHIR endpoint
    :return: Dictionary of important identifier information after validation
    """
    provider_number = None
    npi = None
    for identities in identifier:
        if identities.type and identities.value:
            if is_valid_kaiser_provider_number(identities.value):
                provider_number = identities.value
            else:
                provider_number = "INVALID PROVIDER NUMBER"

        if identities.value and not identities.type:
            npi = validate_npi(identities.value)

    return {"npi": npi, "provider_number": provider_number}


def standardize_data(resource: DomainResource) -> dict:
    """
    Fetches all the important data for practitioner based on the Kaiser data format
    :param resource: Domain Resource from FHIR endpoint
    :return: Compiled important data in standardized format
    """
    name = standardize_name(resource)
    qualifications, licenses = (standardize_qualifications(resource.qualification),
                                standardize_licenses(resource.qualification)) if resource.qualification else (
    None, None)
    identifier = standardize_identifier(resource.identifier) if resource.identifier else None

    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "active": resource.active,
        "name": name,
        "gender": resource.gender,
        "identifier": identifier,
        "qualification": qualifications,
        "licenses": licenses
    }


def fake_Kaydie_time():
    return {
        "id": 'f2e59807-65f8-44c1-a17b-e01d3088a4d9',
        "last_updated": "2023-11-19T00:28:11-04:00",
        "active": True,
        "name": {"first_name": "Kaydie", "middle_name": "L", "last_name": "Satein", "prefix": None, "full_name": None, "qualification": "MD"},
        "gender": "female",
        "identifier": {'npi': '1619302171', 'provider_number': 'EPDM-IND-0000078970'},
        "qualification": {'taxonomy': None, 'display': 'Family Practice-AB Family Medicine'},
        "licenses": [{'state': 'Washington', 'license': 'MD61069302', 'period': {'2020-08-05T00:00:00-07:00', '2024-08-22T00:00:00-07:00'}}]
    }


def fake_Kaydie_active():
    return {
        "id": 'f2e59807-65f8-44c1-a17b-e01d3088a4d9',
        "last_updated": "2023-11-19T00:28:11-07:00",
        "active": False,
        "name": {"first_name": "Kaydie", "middle_name": "L", "last_name": "Satein", "prefix": None, "full_name": None,
                 "qualification": "MD"},
        "gender": "female",
        "identifier": {'npi': '1619302171', 'provider_number': 'EPDM-IND-0000078970'},
        "qualification": {'taxonomy': None, 'display': 'Family Practice-AB Family Medicine'},
        "licenses": [{'state': 'Washington', 'license': 'MD61069302', 'period': {'2020-08-05T00:00:00-07:00', '2024-08-22T00:00:00-07:00'}}]
    }


def fake_Kaydie_licenses():
    return {
        "id": 'f2e59807-65f8-44c1-a17b-e01d3088a4d9',
        "last_updated": "2023-10-20T00:28:11-07:00",
        "active": False,
        "name": {"first_name": "Kaydie", "middle_name": "L", "last_name": "Satein", "prefix": None, "full_name": None, "qualification": "MD"},
        "gender": "female",
        "identifier": {'npi': '1619302171', 'provider_number': 'EPDM-IND-0000078970'},
        "qualification": {'taxonomy': None, 'display': 'Family Practice-AB Family Medicine'},
        "licenses": None
    }


def fake_Kaydie_identifier():
    return {
        "id": 'f2e59807-65f8-44c1-a17b-e01d3088a4d9',
        "last_updated": "2023-10-20T00:28:11-07:00",
        "active": False,
        "name": {"first_name": "Kaydie", "middle_name": "L", "last_name": "Satein", "prefix": None, "full_name": None, "qualification": "MD"},
        "gender": "female",
        "identifier": None,
        "qualification": {'taxonomy': None, 'display': 'Family Practice-AB Family Medicine'},
        "licenses": [{'state': 'Washington', 'license': 'MD61069302', 'period': {'2020-08-05T00:00:00-07:00', '2024-08-22T00:00:00-07:00'}}]
    }


class StandardizedResource:
    def __init__(self, resource: DomainResource):
        """
        Initializes a SmartClient for the given Endpoint. Assumes the Endpoint is properly initialized.
        :param endpoint: A valid Endpoint object
        """
        standardized_resource = standardize_data(resource)

        self.id = standardized_resource.id
        self.last_updated = standardized_resource.last_updated
        self.active: standardized_resource.active
        self.name: standardized_resource.name
        self.gender: standardized_resource.gender
        self.identifier: standardized_resource.identifier
        self.qualification: standardized_resource.qualification
        self.licenses: standardized_resource.licenses
        self.resource: standardized_resource

# def getHumanaData(resource: DomainResource) -> dict:
#     """
#     Fetches all the important data for practitioner based on the Humana data format
#     :param resource: Domain Resource from FHIR endpoint
#     :return: Compiled important data in standardized format
#     """
#     name = get_practitioner_name(resource, "humana")
#     return {
#         "id": resource.id,
#         "last_updated": resource.meta.lastUpdated.isostring,
#         "active": resource.active,
#         "name": name,
#         "gender": resource.gender,
#         "npi": resource.identifier[0].value if resource.identifier[0].value else None
#     }


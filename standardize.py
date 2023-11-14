# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re
from client import validate_npi
from fhirclient.models.domainresource import DomainResource
from typing import List, Tuple


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


def Kaiser_getTaxonomyAndDisplay(qualifications: DomainResource) -> Tuple[str, str]:
    """
    Fetches taxonomy and display values and validates them
    :param qualifications: Qualification Domain Resource from FHIR endpoint
    :return: The taxonomy code and display text
    """
    for qualification in qualifications:
        value = str(qualification.code.coding[0].code)
        if is_valid_taxonomy(value):
            return value, qualification.code.coding[0].display

    return None, None


def Kaiser_getLicenseNumber(qualifications: DomainResource) -> List[str]:
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


def Kaiser_getQualifications(qualifications: DomainResource) -> dict:
    """
    Fetches all the important qualification data and validates them
    :param qualifications: Qualification Domain Resource from FHIR endpoint
    :return: All valid qualification information such as taxonomy and display text
    """
    taxonomy, display = Kaiser_getTaxonomyAndDisplay(qualifications)
    qualifications = {
        "taxonomy": taxonomy,
        "display": display,
    }
    return qualifications


def get_practitioner_name(resource: DomainResource, endpoint: str) -> dict:
    """
    Fetches the practitioner name and normalizes them
    :param resource: Domain Resource from FHIR endpoint
    :param endpoint: Specifies from which endpoint data is being queried from
    :return: The name and other details of the practitioner in standardized format
    """
    first_name, last_name, qualification, prefix, full_name = None, None, None, None, None

    if endpoint == "kaiser":
        if resource.name[0]:
            if resource.name[0].given[0]:
                first_name = resource.name[0].given[0]
                first_name = first_name.split()[0]

            if resource.name[0].family:
                last_name = resource.name[0].family
                last_name = last_name.split()[0]

            if resource.name[0].text:
                qualification = normalize(resource.name[0].text, "qualification")

        return {"first_name": first_name, "last_name": last_name, "qualification": qualification}

    elif endpoint == "humana":
        if resource.name[0]:
            if resource.name[0].given[0]:
                first_name = resource.name[0].given[0]

            if resource.name[0].family:
                last_name = resource.name[0].family

            if resource.name[0].prefix[0]:
                prefix = resource.name[0].prefix[0]

            if resource.name[0].text:
                full_name = resource.name[0].text

        return { "first_name": first_name, "last_name": last_name, "prefix": prefix, "full_name": full_name }

    return None


def Kaiser_getIdentifier(identifier: DomainResource) -> dict:
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

    return { "npi": npi, "provider_number": provider_number }


def getKaiserData(resource: DomainResource) -> dict:
    """
    Fetches all the important data for practitioner based on the Kaiser data format
    :param resource: Domain Resource from FHIR endpoint
    :return: Compiled important data in standardized format
    """
    name = get_practitioner_name(resource, "kaiser")
    qualifications = Kaiser_getQualifications(resource.qualification)
    licenses = Kaiser_getLicenseNumber(resource.qualification)
    identifier = Kaiser_getIdentifier(resource.identifier)

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


def getHumanaData(resource: DomainResource) -> dict:
    """
    Fetches all the important data for practitioner based on the Humana data format
    :param resource: Domain Resource from FHIR endpoint
    :return: Compiled important data in standardized format
    """
    name = get_practitioner_name(resource, "humana")
    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "active": resource.active,
        "name": name,
        "gender": resource.gender,
        "npi": resource.identifier[0].value if resource.identifier[0].value else None
    }

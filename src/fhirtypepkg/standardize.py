# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re
from typing import List, Tuple, Dict, Any

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


def is_valid_provider_number(provider_number: str) -> bool:
    """
    The first four characters and the following three characters must be letters
    The last 10 characters must be digit
    e.g. EPDM-IND-0000149013
    """
    pattern = re.compile(r'^[A-Za-z]{4}-[A-Za-z]{3}-\d{10}$')
    return bool(pattern.match(provider_number))


def standardize_phone_number(phone_number: str) -> str:
    # Remove non-digit characters
    digits_only = re.sub(r"\D", "", phone_number)
    # Add the country code
    formatted_number = "+1" + digits_only

    return formatted_number

def standardize_name(name: str) -> str:
    # Remove "_" and replace with " "
    removed_underscores = re.sub(r'_', ' ', name)
    return removed_underscores

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
            if qualification.code.coding[0].code:
                value = str(qualification.code.coding[0].code)
                value = value if is_valid_taxonomy(value) else None
                if value:
                    display = qualification.code.coding[0].display
                    qualification.code.coding[0].code = value
                    break

    qualifications = {
        "taxonomy": value,
        "display": display,
    }

    return qualifications


def standardize_practitioner_name(resource: DomainResource) -> dict:
    """
    Fetches the practitioner name and normalizes them
    :param resource: Domain Resource from FHIR endpoint
    :return: The name and other details of the practitioner in standardized format
    """
    first_name, middle_name, last_name, qualification, prefix, full_name = None, None, None, None, None, None

    if resource.name:
        name = resource.name[0]

        if name.given:
            first_name = name.given[0]
            first_name = first_name.split()[0]

            if len(first_name.split()) >= 2:
                middle_name = first_name.split()[1]

        if name.family:
            last_name = name.family.strip().split()[0]
            resource.name[0].family = last_name

        if name.prefix:
            prefix = name.prefix[0]

        if name.text:
            full_name = name.text if len(name.text) >= 5 else None
            if not full_name:
                qualification = normalize(name.text, "qualification")
                name.text = qualification
    else:
        return None

    return {"first_name": first_name, "middle_name": middle_name, "last_name": last_name, "prefix": prefix, "full_name": full_name, "qualification": qualification}


def standardize_practitioner_identifier(identifier: DomainResource) -> dict:
    """
    Fetches all the important identifier information and validates them
    :param identifier: Identifier Domain Resource from FHIR endpoint
    :return: Dictionary of important identifier information after validation
    """
    provider_number = None
    npi = None
    for identities in identifier:
        if identities.type and identities.value:
            if is_valid_provider_number(identities.value):
                provider_number = identities.value
            else:
                provider_number = "INVALID PROVIDER NUMBER"

        if identities.value and not identities.type:
            npi = validate_npi(identities.value)

    return {"npi": npi, "provider_number": provider_number}


def standardize_address(resource: DomainResource) -> dict:
    city, district, street, postal_code, state, use, full_address = None, None, None, None, None, None, None

    if resource.address:
        city            = resource.address.city.strip()
        district        = resource.address.district.strip()
        street          = resource.address.line[0].strip()
        postal_code     = resource.address.postalCode.strip()
        state           = resource.address.state.strip()
        use             = resource.address.use.strip()
        full_address    = resource.address.text.strip()

    address = {
        "city"          : city,
        "district"      : district,
        "street"        : street,
        "postal_code"   : postal_code,
        "state"         : state,
        "use"           : use,
        "full_address"  : full_address
    }

    return address


def standardize_position(resource: DomainResource):
    position = resource.position
    if position:
        # TODO: could standardize these coordinates in the future
        return {
            "latitude": position.latitude,
            "longitude": position.longitude
        }
    return None


def standardize_telecom(telecoms: DomainResource):
    phones, faxs = [], []
    for telecom in telecoms:
        if "phone" in telecom.system:
            use = telecom.use
            number = standardize_phone_number(telecom.value)
            telecom.value = number
            phones.append({
                "use": use,
                "number": number
            })
        elif "fax" in telecom.system:
            use = telecom.use
            number = standardize_phone_number(telecom.value)
            telecom.value = number
            faxs.append({
                "use": use,
                "number": number
            })

    return phones, faxs


def standardize_prac_role_organization_identifier(organization: DomainResource) -> dict:
    if organization.identifier:
        system = organization.identifier.system if organization.identifier.system else None
        org_id = organization.identifier.value if organization.identifier.value else None

    return {
        "system": system,
        "org_id": org_id
    }


def standardize_organization_identifier(identifier: DomainResource) -> dict:
    # TODO: when enough data is available, we can assert these values follow a standard
    system = identifier[0].system if identifier[0].system else None
    value = identifier[0].value if identifier[0].value else None

    return {
        "system": system,
        "org_id": value
    }


def standardize_location_identifier(resource: DomainResource):
    # TODO: standardize Facility ID when more data is available
    identifier = resource.identifier[0].value if resource.identifier[0].value else None
    return {"facility_id: ", identifier}


def standardize_practitioner_data(resource: DomainResource) -> tuple[dict[str, dict | None | Any], DomainResource]:
    """
    Fetches all the important data for practitioner and standardizes them and updates the FHIR resource object
    :param resource: Domain Resource from FHIR endpoint
    :return: Compiled important data in standardized format and the updated FHIR resource object
    """
    name = standardize_practitioner_name(resource)
    qualifications, licenses = (standardize_qualifications(resource.qualification), standardize_licenses(resource.qualification)) if resource.qualification else (None, None)
    identifier = standardize_practitioner_identifier(resource.identifier) if resource.identifier else None

    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "active": resource.active,
        "name": name,
        "gender": resource.gender,
        "identifier": identifier,
        "qualification": qualifications,
        "licenses": licenses
    }, resource


def standardize_practitioner_role_data(resource: DomainResource) -> tuple[dict[str, dict | None | Any], DomainResource]:
    """
    Fetches all the important data for practitioner role and standardizes them and updates the FHIR resource object
    :param resource: Domain Resource from FHIR endpoint
    :return: Compiled important data in standardized format and the updated FHIR resource object
    """
    # name = standardize_name(resource)
    # qualifications, licenses = (standardize_qualifications(resource.qualification), standardize_licenses(resource.qualification)) if resource.qualification else (None, None)
    # identifier = standardize_identifier(resource.identifier) if resource.identifier else None

    org_identifier = standardize_prac_role_organization_identifier(resource.organization)
    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "language": resource.language,
        "active": resource.active,
        "identifier": org_identifier
    }, resource


def standardize_organization_data(resource: DomainResource) -> tuple[dict[str, dict | None | Any], DomainResource]:
    """

    :param resource:
    :return:
    """
    identifier  = standardize_organization_identifier(resource.identifier)
    org_name        = standardize_name(resource.name)
    resource.name   = org_name
    return {
        "id"            : resource.id,
        "language"      : resource.language,
        "last_updated"  : resource.meta.lastUpdated.isostring,
        "active"        : resource.active,
        "identifier"    : identifier,
        "name"          : org_name
    }, resource


def standardize_location_data(resource: DomainResource) -> tuple[dict[str, dict | None | Any], DomainResource]:
    """

    :param resource:
    :return:
    """
    address         = standardize_address(resource)
    identifier      = standardize_location_identifier(resource)
    position        = standardize_position(resource)
    phones, faxs         = standardize_telecom(resource.telecom)
    return {
        "id"            : resource.id,
        "language"      : resource.language,
        "last_updated"  : resource.meta.lastUpdated.isostring,
        "status"        : resource.status,
        "address"       : address,
        "identifier"    : identifier,
        "name"          : resource.name if resource.name else None,
        "position"      : position,
        "phone_numbers" : phones,
        "fax_numbers"   : faxs
    }, resource


class StandardizedResource:
    def __init__(self, resource: DomainResource):
        """
        Initializes a SmartClient for the given Endpoint. Assumes the Endpoint is properly initialized.
        It has the following values which are accessible:
        """

        # standardized_practitioner, resource = standardize_practitioner_data(resource)

        self.PRACTITIONER       = None
        self.PRACTITIONER_ROLE  = None
        self.LOCATION           = None
        self.ORGANIZATION       = None
        self.RESOURCE           = resource

    def setPractitioner(self, resource: DomainResource):
        standardized_practitioner, resource = standardize_practitioner_data(resource)
        self.PRACTITIONER                   = self.Practitioner(standardized_practitioner)
        self.RESOURCE                       = resource

    def setPractitionerRole(self, resource: DomainResource):
        standardized_practitioner_role, resource    = standardize_practitioner_role_data(resource)
        self.PRACTITIONER_ROLE                      = self.PractitionerRole(standardized_practitioner_role)
        self.RESOURCE                               = resource

    def setLocation(self, resource: DomainResource):
        standardized_location, resource = standardize_location_data(resource)
        self.LOCATION                   = self.Location(standardized_location)
        self.RESOURCE                   = resource

    def setOrganization(self, resource: DomainResource):
        standardized_location, resource = standardize_organization_data(resource)
        self.ORGANIZATION = self.Organization(standardized_location)
        self.RESOURCE = resource

    class Practitioner:
        """
        It has the following values which are accessible:
            self. id
            self. last_updated
            self. active
            self. name
            self. gender
            self. identifier
            self. qualification
            self. licenses
            self. filtered_dictionary - this will be used by the consensus model
        """
        def __init__(self, standardized_practitioner):
            # updates the instance variables in one go
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class PractitionerRole:
        def __init__(self, standardized_practitioner):
            # updates the instance variables in one go
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class Location:
        def __init__(self, standardized_practitioner):
            # updates the instance variables in one go
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class Organization:
        def __init__(self, standardized_practitioner):
            # updates the instance variables in one go
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner


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
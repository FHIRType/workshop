# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re
from typing import List, Tuple, Dict, Any

from fhirclient.models.fhirreference import FHIRReference

from src.fhirtypepkg.fhirtype import ExceptionNPI
from fhirclient.models.domainresource import DomainResource

KEY_ID = "id"
KEY_LANGUAGE = "language"
KEY_LAST_UPDATED = "last_updated"
KEY_STATUS = "status"
KEY_ADDRESS = "address"
KEY_IDENTIFIER = "identifier"
KEY_NAME = "name"
KEY_POSITION = "position"
KEY_PHONE_NUMBERS = "phone_numbers"
KEY_FAX_NUMBERS = "fax_numbers"
KEY_ACTIVE = "active"
KEY_TAXONOMY = "taxonomy"
KEY_DISPLAY = "display"
KEY_PERIOD = "period"
KEY_QUALIFICATION = "qualification"
KEY_STATE = "state"
KEY_LICENSE = "license"
KEY_LICENSES = "licenses"
KEY_FIRST_NAME = "first_name"
KEY_MIDDLE_NAME = "middle_name"
KEY_LAST_NAME = "last_name"
KEY_PREFIX = "prefix"
KEY_FULL_NAME = "full_name"
KEY_NPI = "npi"
KEY_PROVIDER_NUMBER = "provider_number"
KEY_CITY = "city"
KEY_DISTRICT = "district"
KEY_STREET = "street"
KEY_POSTAL_CODE = "postal_code"
KEY_USE = "use"
KEY_FULL_ADDRESS = "full_address"
KEY_LATITUDE = "latitude"
KEY_LONGITUDE = "longitude"
KEY_NUMBER = "number"
KEY_SYSTEM = "system"
KEY_ORGANIZATION_ID = "org_id"
KEY_FACILITY_ID = "facility_id"
KEY_GENDER = "gender"

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
    if value_type == KEY_QUALIFICATION:
        return value.strip(", ")

    # more datatype can be specified here if needed in future


def standardize_licenses(qualifications: DomainResource) -> List[str]:
    """
    Fetches all the license numbers from the given qualifications and validates them.

    Parameters:
    :param qualifications: The qualifications to fetch license numbers from.
    :type qualifications: DomainResource

    Returns:
    :return: A list of all found licenses, or None if no licenses were found.
    :rtype: List[str]
    """
    licenses = []

    for qualification in qualifications:
        license_details = {}
        if qualification.extension:
            for extension in qualification.extension:
                if extension.valueCodeableConcept:
                    license_details[
                        KEY_STATE
                    ] = extension.valueCodeableConcept.coding[
                        0
                    ].display

        if qualification.identifier:
            license_valid = is_valid_license(qualification.identifier[0].value)
            if license_valid:
                license_details[KEY_LICENSE] = qualification.identifier[
                    0
                ].value
            else:
                license_details[
                    KEY_LICENSE
                ] = "INVALID LICENSE NUMBER"

        if qualification.period:
            period = {
                qualification.period.start.isostring
                if qualification.period.start is not None
                else None,
                qualification.period.end.isostring
                if qualification.period.end is not None
                else None,
            }
            license_details[KEY_PERIOD] = period

        # only append if not empty
        if license_details:
            licenses.append(license_details)

    if licenses:
        return licenses
    else:
        return None


def standardize_qualifications(qualifications: DomainResource) -> dict:
    """
    Fetches all the important qualification data from the given qualifications and validates them.

    Parameters:
    :param qualifications: The qualifications to fetch data from.
    :type qualifications: DomainResource

    Returns:
    :return: A dictionary containing all valid qualification information, such as taxonomy and display text.
    :rtype: dict
    """
    taxonomy, display = None, None

    for qualification in qualifications:
        if qualification.code.coding:
            if qualification.code.coding[0].code:
                value = str(qualification.code.coding[0].code)
                value = value if is_valid_taxonomy(value) else None
                if value:
                    display = qualification.code.coding[0].display
                    qualification.code.coding[0].code = value

                    qualifications = {
                        KEY_TAXONOMY: value,
                        KEY_DISPLAY: display,
                    }
                    break

    return qualifications


def standardize_practitioner_name(resource: DomainResource) -> dict:
    """
    Fetches the practitioner's name from the given resource and normalizes it.

    Parameters:
    :param resource: The resource to fetch the practitioner's name from.
    :type resource: DomainResource

    Returns:
    :return: A dictionary containing the practitioner's first name, middle name, last name, prefix, full name, and qualification, all in a standardized format.
    :rtype: dict
    """
    first_name, middle_name, last_name, qualification, prefix, full_name = (
        None,
        None,
        None,
        None,
        None,
        None,
    )

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
                qualification = normalize(
                    name.text, KEY_QUALIFICATION
                )
                name.text = qualification
    else:
        return None

    return {
        KEY_FIRST_NAME: first_name,
        KEY_MIDDLE_NAME: middle_name,
        KEY_LAST_NAME: last_name,
        KEY_PREFIX: prefix,
        KEY_FULL_NAME: full_name,
        KEY_QUALIFICATION: qualification,
    }


def standardize_practitioner_identifier(identifier: DomainResource) -> dict:
    """
    Fetches all the important identifier information from the given identifier and validates them.

    Parameters:
    :param identifier: The identifier to fetch data from.
    :type identifier: DomainResource

    Returns:
    :return: A dictionary containing important identifier information after validation.
    :rtype: dict
    """
    provider_number = None
    npi = None
    for identities in identifier:
        if identities.type and identities.value:
            if is_valid_provider_number(identities.value):
                provider_number = identities.value
            else:
                provider_number = "INVALID PROVIDER NUMBER"

        if (
            identities.value
            and not identities.type):
            if identities.system == "http://hl7.org/fhir/sid/us-npi":
              npi = validate_npi(identities.value)
            else:
                npi = "NPI is not in FHIR standard code system for the NPI in the U.S"

    return {KEY_NPI: npi, KEY_PROVIDER_NUMBER: provider_number}


def standardize_address(resource: DomainResource) -> dict:
    """
    Fetches the address from the given resource and standardizes it.

    Parameters:
    :param resource: The resource to fetch the address from.
    :type resource: DomainResource

    Returns:
    :return: A dictionary containing the city, district, street, postal code, state, use, and full address, all in a standardized format.
    :rtype: dict
    """
    city, district, street, postal_code, state, use, full_address = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    if resource.address:
        city = resource.address.city.strip() if resource.address.city else None
        district = resource.address.district.strip() if resource.address.district else None
        street = resource.address.line[0].strip() if resource.address.line else None
        postal_code = resource.address.postalCode.strip() if resource.address.postalCode else None
        state = resource.address.state.strip() if resource.address.state else None
        use = resource.address.use.strip() if resource.address.use else None
        full_address = resource.address.text.strip() if resource.address.text else None

    address = {
        KEY_CITY: city,
        KEY_DISTRICT: district,
        KEY_STREET: street,
        KEY_POSTAL_CODE: postal_code,
        KEY_STATE: state,
        KEY_USE: use,
        KEY_FULL_ADDRESS: full_address,
    }

    return address


def standardize_position(resource: DomainResource) -> dict or None:
    """
    Fetches the position from the given resource.

    Parameters:
    :param resource: The resource to fetch the position from.
    :type resource: DomainResource

    Returns:
    :return: A dictionary containing the latitude and longitude.
    :rtype: dict
    """
    if resource.position:
        # TODO: could standardize these coordinates in the future
        return {
            KEY_LATITUDE: resource.position.latitude if resource.position.latitude else None,
            KEY_LONGITUDE: resource.position.longitude if resource.position.longitude else None
        }
    return None


def standardize_telecom(telecoms: DomainResource) -> list:
    """
    Fetches the telecom information from the given telecoms and standardizes it.

    Parameters:
    :param telecoms: The telecoms to fetch data from.
    :type telecoms: DomainResource

    Returns:
    :return: Two lists containing phone numbers and fax numbers.
    :rtype: tuple
    """
    phones, faxs, number = None, None, None
    if telecoms is not None:
        phones, faxs = [], []
        for telecom in telecoms:
            if "phone" in telecom.system:
                use = telecom.use if telecom.use else None
                if telecom.value:
                    number = standardize_phone_number(telecom.value)
                    telecom.value = number
                phones.append({KEY_USE: use, KEY_NUMBER: number})
            elif "fax" in telecom.system:
                use = telecom.use  if telecom.use else None
                if telecom.value:
                    number = standardize_phone_number(telecom.value)
                    telecom.value = number
                faxs.append({KEY_USE: use, KEY_NUMBER: number})

    return phones, faxs


def standardize_prac_role_organization_identifier(organization: DomainResource) -> dict:
    """
    Fetches the organization identifier from the given organization and standardizes it.

    Parameters:
    :param organization: The organization to fetch the identifier from.
    :type organization: DomainResource

    Returns:
    :return: A dictionary containing the system and organization ID.
    :rtype: dict
    """
    system, org_id = None, None

    # TODO: If identifier is a list, handle each

    if organization.identifier:
        if type(organization.identifer):
            for identify in organization.identifier:
                system = (
                    identify.system if identify.system else None
                )
                org_id = (
                    identify.value if identify.value else None
                )
        else:
            system = (
                organization.identifier.system if organization.identifier.system else None
            )
            org_id = (
                organization.identifier.value if organization.identifier.value else None
            )

    return {KEY_SYSTEM: system, KEY_ORGANIZATION_ID: org_id}


def standardize_organization_identifier(identifier: DomainResource) -> dict:
    """
    Fetches the organization identifier from the given identifier and standardizes it.

    Parameters:
    :param identifier: The identifier to fetch data from.
    :type identifier: DomainResource

    Returns:
    :return: A dictionary containing the system and organization ID.
    :rtype: dict
    """
    # TODO: when enough data is available, we can assert these values follow a standard
    system = identifier[0].system if identifier[0].system else None
    value = identifier[0].value if identifier[0].value else None

    return {KEY_SYSTEM: system, KEY_ORGANIZATION_ID: value}


def standardize_location_identifier(resource: DomainResource) -> dict:
    """
    Fetches the location identifier from the given resource.

    Parameters:
    :param resource: The resource to fetch the location identifier from.
    :type resource: DomainResource

    Returns:
    :return: A dictionary containing the facility ID.
    :rtype: dict
    """
    # TODO: standardize Facility ID when more data is available
    identifier = None

    if resource.identifier is not None:
        identifier = resource.identifier[0].value if resource.identifier[0].value else None

    return {KEY_FACILITY_ID: identifier}


def standardize_practitioner_data(
    resource: DomainResource,
) -> tuple[dict, DomainResource]:
    """
    Fetches all the important data for a practitioner from the given resource, standardizes it, and updates the FHIR resource object.

    Parameters:
    :param resource: The resource to fetch data from.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing a dictionary of important data in a standardized format and the updated FHIR resource object.
    :rtype: tuple
    """
    name = standardize_practitioner_name(resource)
    qualifications, licenses = (
        (
            standardize_qualifications(resource.qualification),
            standardize_licenses(resource.qualification),
        )
        if resource.qualification
        else (None, None)
    )
    identifier = (
        standardize_practitioner_identifier(resource.identifier)
        if resource.identifier
        else None
    )

    return {
        KEY_ID: resource.id,
        KEY_LAST_UPDATED: resource.meta.lastUpdated.isostring,
        KEY_ACTIVE: resource.active if resource.active else None,
        KEY_NAME: name,
        KEY_GENDER: resource.gender if resource.gender else None,
        KEY_IDENTIFIER: identifier,
        KEY_QUALIFICATION: qualifications,
        KEY_LICENSES: licenses,
    }, resource


def standardize_practitioner_role_data(
    resource: DomainResource,
) -> tuple[dict, DomainResource]:
    """
    Fetches all the important data for a practitioner role from the given resource, standardizes it, and updates the FHIR resource object.

    Parameters:
    :param resource: The resource to fetch data from.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing a dictionary of important data in a standardized format and the updated FHIR resource object.
    :rtype: tuple
    """
    org_identifier = None

    # at this point, we either have an org DR or a None
    #
    # if resource.organization is not None:
    #     org_identifier = standardize_prac_role_organization_identifier(
    #         resource.organization
    #     )

    return {
        KEY_ID: resource.id,
        KEY_LAST_UPDATED: resource.meta.lastUpdated.isostring,
        KEY_LANGUAGE: resource.language if resource.language else None,
        KEY_ACTIVE: resource.active if resource.active else None,  # TODO: Active is a shall have
        KEY_IDENTIFIER: org_identifier
    }, resource


def standardize_organization_data(
    resource: DomainResource,
) -> tuple[dict, DomainResource]:
    """
    Fetches all the important data for an organization from the given resource, standardizes it, and updates the FHIR resource object.

    Parameters:
    :param resource: The resource to fetch data from.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing a dictionary of important data in a standardized format and the updated FHIR resource object.
    :rtype: tuple
    """
    identifier = standardize_organization_identifier(resource.identifier) if False else "None" # overriding standardizaiton
    org_name = standardize_name(resource.name)  if False else "None" # overriding standardizaiton
    # resource.name = org_name
    return {
        KEY_ID: resource.id,
        KEY_LANGUAGE: resource.language if resource.language else None,
        KEY_LAST_UPDATED: resource.meta.lastUpdated.isostring,
        KEY_ACTIVE: resource.active if resource.active else None,
        KEY_IDENTIFIER: identifier,
        KEY_NAME: org_name,
    }, resource


def standardize_location_data(resource: DomainResource) -> tuple[dict, DomainResource]:
    """
    Fetches all the important data for a location from the given resource, standardizes it, and updates the FHIR resource object.

    Parameters:
    :param resource: The resource to fetch data from.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing a dictionary of important data in a standardized format and the updated FHIR resource object.
    :rtype: tuple
    """
    address = standardize_address(resource)
    identifier = standardize_location_identifier(resource)
    position = standardize_position(resource)
    phones, faxs = standardize_telecom(resource.telecom)
    return {
        KEY_ID: resource.id,
        KEY_LANGUAGE: resource.language if resource.language else None,
        KEY_LAST_UPDATED: resource.meta.lastUpdated.isostring,
        KEY_STATUS: resource.status if resource.status else None,
        KEY_ADDRESS: address,
        KEY_IDENTIFIER: identifier,
        KEY_NAME: resource.name if resource.name else None,
        KEY_POSITION: position,
        KEY_PHONE_NUMBERS: phones,
        KEY_FAX_NUMBERS: faxs,
    }, resource


class StandardizedResource:
    """
    A class used to represent a Standardized Resource.

    Attributes
    ----------
    PRACTITIONER : Practitioner
        an instance of the Practitioner class representing a standardized practitioner
    PRACTITIONER_ROLE : PractitionerRole
        an instance of the PractitionerRole class representing a standardized practitioner role
    LOCATION : Location
        an instance of the Location class representing a standardized location
    ORGANIZATION : Organization
        an instance of the Organization class representing a standardized organization
    RESOURCE : DomainResource
        the original resource object

    Methods
    -------
    setPractitioner(resource: DomainResource)
        Standardizes the given practitioner resource and sets the PRACTITIONER attribute.
    setPractitionerRole(resource: DomainResource)
        Standardizes the given practitioner role resource and sets the PRACTITIONER_ROLE attribute.
    setLocation(resource: DomainResource)
        Standardizes the given location resource and sets the LOCATION attribute.
    setOrganization(resource: DomainResource)
        Standardizes the given organization resource and sets the ORGANIZATION attribute.
    """

    def __init__(self):
        """
        Initializes a new instance of the StandardizedResource class.
        """
        self.PRACTITIONER = None
        self.PRACTITIONER_ROLE = None
        self.LOCATION = None
        self.ORGANIZATION = None
        self.RESOURCE = None

    def setPractitioner(self, resource: DomainResource):
        """
        Standardizes the given practitioner resource and sets the PRACTITIONER attribute.

        Parameters:
        :param resource: The resource to standardize.
        :type resource: DomainResource
        """
        standardized_practitioner, resource = standardize_practitioner_data(resource)
        self.PRACTITIONER = self.Practitioner(standardized_practitioner)
        self.RESOURCE = resource

    def setPractitionerRole(self, resource: DomainResource):
        """
        Standardizes the given practitioner role resource and sets the PRACTITIONER_ROLE attribute.

        Parameters:
        :param resource: The resource to standardize.
        :type resource: DomainResource
        """
        standardized_practitioner_role, resource = standardize_practitioner_role_data(
            resource
        )
        self.PRACTITIONER_ROLE = self.PractitionerRole(standardized_practitioner_role)
        self.RESOURCE = resource

    def setLocation(self, resource: DomainResource):
        """
        Standardizes the given location resource and sets the LOCATION attribute.

        Parameters:
        :param resource: The resource to standardize.
        :type resource: DomainResource
        """
        standardized_location, resource = standardize_location_data(resource)
        self.LOCATION = self.Location(standardized_location)
        self.RESOURCE = resource

    def setOrganization(self, resource: DomainResource):
        """
        Standardizes the given organization resource and sets the ORGANIZATION attribute.

        Parameters:
        :param resource: The resource to standardize.
        :type resource: DomainResource
        """
        standardized_location, resource = standardize_organization_data(resource)
        self.ORGANIZATION = self.Organization(standardized_location)
        self.RESOURCE = resource

    class Practitioner:
        """
        A class used to represent a Standardized Practitioner.

        Attributes
        ----------
        id : str
            The ID of the practitioner.
        last_updated : str
            The last updated timestamp of the practitioner.
        active : bool
            The active status of the practitioner.
        name : str
            The name of the practitioner.
        gender : str
            The gender of the practitioner.
        identifier : dict
            The identifier of the practitioner.
        qualification : list
            The qualifications of the practitioner.
        licenses : list
            The licenses of the practitioner.
        filtered_dictionary : dict
            A dictionary of the practitioner's attributes for use by the consensus model.

        Methods
        -------
        __init__(self, standardized_practitioner: dict)
            Initializes a new instance of the Practitioner class.
        """

        def __init__(self, standardized_practitioner):
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class PractitionerRole:
        """
        A class used to represent a Standardized Practitioner Role.

        Attributes are similar to the Practitioner class.

        Methods
        -------
        __init__(self, standardized_practitioner: dict)
            Initializes a new instance of the PractitionerRole class.
        """

        def __init__(self, standardized_practitioner):
            """
            Initializes a new instance of the PractitionerRole class.

            Parameters:
            :param standardized_practitioner: The standardized practitioner role data.
            :type standardized_practitioner: dict
            """
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class Location:
        """
        A class used to represent a Standardized Location.

        Attributes are similar to the Practitioner class.

        Methods
        -------
        __init__(self, standardized_practitioner: dict)
            Initializes a new instance of the Location class.
        """

        def __init__(self, standardized_practitioner):
            """
            Initializes a new instance of the Location class.

            Parameters:
            :param standardized_practitioner: The standardized location data.
            :type standardized_practitioner: dict
            """
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

    class Organization:
        """
        A class used to represent a Standardized Organization.

        Attributes are similar to the Practitioner class.

        Methods
        -------
        __init__(self, standardized_practitioner: dict)
            Initializes a new instance of the Organization class.
        """

        def __init__(self, standardized_practitioner):
            """
            Initializes a new instance of the Organization class.

            Parameters:
            :param standardized_practitioner: The standardized organization data.
            :type standardized_practitioner: dict
            """
            self.__dict__.update(standardized_practitioner)
            self.filtered_dictionary = standardized_practitioner

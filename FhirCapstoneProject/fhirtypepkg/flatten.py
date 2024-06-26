import re
from datetime import datetime, timezone
from typing import List, Dict, Any
from typing import Optional

from fhirclient.models.domainresource import DomainResource
from pydantic import BaseModel

from FhirCapstoneProject.fhirtypepkg.fhirtype import ExceptionNPI


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


def is_valid_taxonomy(taxonomy: str) -> bool:
    """
    Checks if the given taxonomy is valid.

    A valid taxonomy must start with exactly 9 digits, followed by a single letter, or start with at least 3 digits, followed by at least 1 letter, followed by at least 1 digit, and ending with the character "X".
    For example, a valid taxonomy could be "104100000X" or "103TC2200X".

    Parameters:
    :param taxonomy: The taxonomy to validate.
    :type taxonomy: str

    Returns:
    :return: True if the taxonomy is valid, False otherwise.
    :rtype: bool
    """
    pattern = re.compile(r"^\d{9}[A-Za-z]{1}$|^\d{3,}[A-Za-z]+\d{1,}X$")
    return bool(pattern.match(taxonomy))


def standardize_phone_number(phone_number: str) -> str:
    """
    Standardizes phone numbers to a uniform format by removing non-numeric characters.

    Parameters:
    :param phone_number: The phone number to standardize.
    :type phone_number: str

    Returns:
    :return: A standardized phone number string containing only numeric characters.
    :rtype: str
    """
    # Remove any character that is not a digit
    standardized_phone = re.sub(r"[^\d]", "", phone_number)

    return standardized_phone


def get_name(resource, sub_attr: str = None):
    """
    Retrieves the name from a given resource object based on specified attributes.

    This function attempts to access the "name" attribute of the resource object and returns the full name,
    first name, or last name depending on the value of sub_attr.

    Parameters:
    :param resource: The resource object containing the name attribute.
    :type resource: object
    :param sub_attr: The specific part of the name to retrieve ('full', 'first', 'last'). Defaults to None.
    :type sub_attr: str, optional

    Returns:
    :return: The requested name part from the resource, or None if not available.
    :rtype: str

    Raises:
    None
    """
    if hasattr(resource, "name"):
        name_obj = getattr(resource, "name", [])
        name_obj = name_obj[0]  # Assuming the first name object is the one we want
        if sub_attr == "full":
            full_name = name_obj.family or None
            given_names = " ".join(name_obj.given) if name_obj.given else None
            if given_names:
                full_name += ", " + given_names
            return full_name
        elif sub_attr == "first":
            return (
                re.split(r"[^a-zA-Z]", name_obj.given[0])[0].capitalize()
                if name_obj.given
                else None
            )
        elif sub_attr == "last":
            # Split by anything other than a letter
            return name_obj.family.capitalize() or None
    return None


def get_npi(resource):
    """
    Retrieves and validates the National Provider Identifier (NPI) from a given resource object.

    This function attempts to access the "identifier" attribute of the resource object and returns
    the validated NPI if it exists and matches the required system.

    Parameters:
    :param resource: The resource object containing the identifier attribute.
    :type resource: object

    Returns:
    :return: The validated NPI from the resource, or None if not available.
    :rtype: str

    Raises:
    None
    """
    if hasattr(resource, "identifier"):
        field_value = getattr(resource, "identifier", [])
        if field_value is None:
            return None
        for identifier in field_value:
            if identifier.system == "http://hl7.org/fhir/sid/us-npi":
                return validate_npi(identifier.value)
    return None


def get_taxonomy(qualification_obj):
    """
    Retrieves and validates the taxonomy code from a given qualification object.

    This function attempts to access the "qualification" attribute of the qualification object and returns
    the validated taxonomy code if it exists and matches the required system.

    Parameters:
    :param qualification_obj: The qualification object containing the code attribute.
    :type qualification_obj: object

    Returns:
    :return: The validated taxonomy code from the qualification object, or a message indicating if not found or invalid.
    :rtype: str

    Raises:
    None
    """
    if qualification_obj is None:
        return "Taxonomy not found"
    for qualification in qualification_obj:
        for coding in qualification.code.coding:
            if coding.system == "http://nucc.org/provider-taxonomy":
                _validity = is_valid_taxonomy(coding.code)
                if _validity:
                    return coding.code
                return "Invalid Taxonomy: " + coding.code
    return None


def get_address(address_obj, sub_attr: str = None):
    """
    Retrieves a specific part of the address from a given address object.

    This function attempts to access the "text" attribute of the first address in the address object
    and returns the requested part of the address based on the value of sub_attr.

    Parameters:
    :param address_obj: The address object containing the address attributes.
    :type address_obj: object
    :param sub_attr: The specific part of the address to retrieve ('street', 'city', 'state', 'zip'). Defaults to None.
    :type sub_attr: str, optional

    Returns:
    :return: The requested part of the address, or None if not available.
    :rtype: str

    Raises:
    None
    """
    if address_obj:
        address = address_obj[0]  # assumption made here
        if address.text:
            if sub_attr == "street":
                return address.text.split(",")[0]
            elif sub_attr == "city":
                return address.text.split(",")[1]
            elif sub_attr == "state":
                return address.text.split(",")[2]
            elif sub_attr == "zip":
                return address.text.split(",")[3]
    return None


def get_role_taxonomy(resource: DomainResource):
    """
    Retrieves the taxonomy code from the specialty attribute of a given resource object.

    This function checks the "specialty" attribute of the resource object and returns the taxonomy code
    if it exists and matches the required system.

    Parameters:
    :param resource: The resource object containing the specialty attribute.
    :type resource: DomainResource

    Returns:
    :return: The taxonomy code from the specialty attribute, or None if not available.
    :rtype: str

    Raises:
    None
    """
    # Check if 'specialty' is present in the resource
    if hasattr(resource, "specialty") and resource.specialty:
        for specialty in resource.specialty:
            # Directly access the 'coding' attribute as it's an attribute of the 'CodeableConcept' object
            if hasattr(specialty, "coding") and specialty.coding:
                for code in specialty.coding:
                    # Check if 'system' is the one we're interested in
                    if (
                        hasattr(code, "system")
                        and code.system == "http://nucc.org/provider-taxonomy"
                    ):
                        return code.code
    return None


def get_loc_address(resource: DomainResource):
    """
    Retrieves the address components from a given resource object.

    This function checks the "address" attribute of the resource object and returns the address components
    such as street address, city, state, and zip code if they exist.

    Parameters:
    :param resource: The resource object containing the address attribute.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing the street address, city, state, and zip code.
    :rtype: tuple

    Raises:
    None
    """
    add1 = city = state = zip_code = None  # Default values
    if hasattr(resource, "address") and resource.address:
        address = resource.address  # Direct access without assuming it's a list

        # Direct attribute access with hasattr checks
        city = address.city if hasattr(address, "city") else "Optional"
        state = address.state if hasattr(address, "state") else "Optional"
        zip_code = address.postalCode if hasattr(address, "postalCode") else "Optional"

        # Handle 'line' which is expected to be a list
        if hasattr(address, "line") and address.line:
            add1 = address.line[0]  # Taking the first line as the primary address

    return add1, city, state, zip_code


def get_loc_telecom(resource):
    """
    Retrieves the telecom contact details from a given resource object.

    This function checks the "telecom" attribute of the resource object and returns the contact details
    such as phone, fax, and email if they exist.

    Parameters:
    :param resource: The resource object containing the telecom attribute.
    :type resource: object

    Returns:
    :return: A tuple containing the phone number, fax number, and email address.
    :rtype: tuple

    Raises:
    None
    """
    phone = fax = email = None
    if hasattr(resource, "telecom") and resource.telecom:
        for contact in resource.telecom:
            system = contact.system.lower() if hasattr(contact, "system") else ""
            value = contact.value if hasattr(contact, "value") else "Optional"
            if system == "phone":
                phone = standardize_phone_number(value)
            elif system == "fax":
                fax = standardize_phone_number(value)
            elif system == "email":
                email = value
    return phone, fax, email


def get_loc_coordinates(resource: DomainResource):
    """
    Retrieves the geographic coordinates from a given resource object.

    This function checks the "position" attribute of the resource object and returns the latitude and longitude
    if they exist.

    Parameters:
    :param resource: The resource object containing the position attribute.
    :type resource: DomainResource

    Returns:
    :return: A tuple containing the latitude and longitude.
    :rtype: tuple

    Raises:
    None
    """
    lat = lng = None
    # Check if the resource has a 'position' attribute and both 'latitude' and 'longitude' are present
    if (
        hasattr(resource, "position")
        and hasattr(resource.position, "latitude")
        and hasattr(resource.position, "longitude")
    ):
        lat = resource.position.latitude
        lng = resource.position.longitude

    return lat, lng


def get_org_name(resource: DomainResource):
    """
    Retrieves the organization name from a given resource object.

    This function checks the "organization" attribute of the resource object and returns the name
    if it exists, replacing underscores with spaces.

    Parameters:
    :param resource: The resource object containing the organization attribute.
    :type resource: DomainResource

    Returns:
    :return: The organization name, or None if not available.
    :rtype: str

    Raises:
    None
    """
    name = None
    if resource.organization and hasattr(resource.organization, "name"):
        name = resource.organization.name
        name = name.replace("_", " ")

    return name


def flatten_prac(resource: DomainResource):
    """
    Flattens the practitioner resource into a dictionary with key attributes.

    This function extracts specific attributes from the practitioner resource object and returns
    them in a dictionary format.

    Parameters:
    :param resource: The resource object containing practitioner details.
    :type resource: DomainResource

    Returns:
    :return: A dictionary with flattened practitioner attributes.
    :rtype: dict

    Raises:
    None
    """
    gender = resource.gender.capitalize() if resource.gender else None
    last_update = (
        resource.meta.lastUpdated.isostring
        if hasattr(resource, "meta") and hasattr(resource.meta, "lastUpdated")
        else None
    )
    return {
        "FullName": get_name(resource, "full"),
        "NPI": get_npi(resource),
        "FirstName": get_name(resource, "first"),
        "LastName": get_name(resource, "last"),
        "Gender": gender,
        "LastPracUpdate": last_update,
    }


def flatten_role(resource: DomainResource):
    """
    Flattens the role resource into a dictionary with key attributes.

    This function extracts specific attributes from the role resource object and returns
    them in a dictionary format.

    Parameters:
    :param resource: The resource object containing role details.
    :type resource: DomainResource

    Returns:
    :return: A dictionary with flattened role attributes.
    :rtype: dict

    Raises:
    None
    """
    last_update = (
        resource.meta.lastUpdated.isostring
        if hasattr(resource, "meta") and hasattr(resource.meta, "lastUpdated")
        else None
    )

    org_name = get_org_name(resource=resource)

    return {
        "GroupName": org_name,
        "Taxonomy": get_role_taxonomy(resource),
        "LastPracRoleUpdate": last_update,
    }


def flatten_loc(resource: DomainResource):
    """
    Flattens the location resource into a dictionary with key attributes.

    This function extracts specific attributes from the location resource object and returns
    them in a dictionary format.

    Parameters:
    :param resource: The resource object containing location details.
    :type resource: DomainResource

    Returns:
    :return: A dictionary with flattened location attributes.
    :rtype: dict

    Raises:
    None
    """
    add1, city, state, zip_code = get_loc_address(resource)
    phone, fax, email = get_loc_telecom(resource)
    lat, lng = get_loc_coordinates(resource)
    last_update = (
        resource.meta.lastUpdated.isostring
        if hasattr(resource, "meta") and hasattr(resource.meta, "lastUpdated")
        else None
    )
    return {
        "ADD1": add1,
        "ADD2": None,
        "City": city,
        "State": state,
        "Zip": zip_code,
        "Phone": phone,
        "Fax": fax,
        "Email": email,
        "lat": lat,
        "lng": lng,
        "LastLocationUpdate": last_update,
    }


class FlattenSmartOnFHIRObject:
    """
    Deserializes SmartOnFHIR Objects into a structured JSON format.
    Stores flattened practitioner, role, and location data.
    ----

    Attributes:
        :param metadata: A dictionary storing metadata information such as endpoint and date retrieved.
        :type metadata: dict
        :param prac_obj: A practitioner object.
        :type prac_obj: object
        :param prac_role_obj: A list of practitioner role objects.
        :type prac_role_obj: list
        :param prac_loc_obj: A list of practitioner location objects.
        :type prac_loc_obj: list
        :param flatten_prac: A list to store flattened practitioner data.
        :type flatten_prac: list
        :param flatten_prac_role: A list to store flattened practitioner role data.
        :type flatten_prac_role: list
        :param flatten_prac_loc: A list to store flattened practitioner location data.
        :type flatten_prac_loc: list
        :param flatten_data: A dictionary to store the final flattened data.
        :type flatten_data: dict
    """

    def __init__(self, endpoint: str) -> None:
        """
        Initializes the FlattenSmartOnFHIRObject with the given endpoint.

        Parameters:
        :param endpoint: The endpoint URL.
        :type endpoint: str
        """
        self.metadata = {
            "Endpoint": endpoint,
            "DateRetrieved": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            + "Z",
            "Accuracy": -1.0,
        }
        self.prac_obj = None
        self.prac_role_obj: List = []
        self.prac_loc_obj: List = []

        # Flatten related declarations
        self.flatten_prac = []
        self.flatten_prac_role: List = []
        self.flatten_prac_loc: List = []
        self.flatten_data = {}

    def flatten_all(self) -> None:
        """
        Processes and flattens FHIR Client objects for practitioners, their roles, and locations into structured data.
        """

        from collections import defaultdict

        # Initialize a temporary data holder as defaultdict to handle missing keys smoothly
        combined_data = defaultdict(lambda: None, **self.metadata)

        # Flatten the practitioner object if it exists
        if self.prac_obj:
            prac_data = flatten_prac(resource=self.prac_obj)
            for key, value in prac_data.items():
                combined_data[key] = value

        # Flatten roles and collect necessary data
        if self.prac_role_obj:
            for role in self.prac_role_obj:
                role_data = flatten_role(resource=role)
                for key, value in role_data.items():
                    combined_data[key] = value

        # Flatten the locations
        if self.prac_loc_obj:
            for loc in self.prac_loc_obj:
                loc_data = flatten_loc(resource=loc)
                for key, value in loc_data.items():
                    combined_data[key] = value

        self.flatten_data = StandardProcessModel(**combined_data).model_dump()

    def get_flattened_data(self) -> Dict[str, Any]:
        """
        Returns the flattened data.

        Returns:
        :return: The flattened data.
        :rtype: dict
        """
        return self.flatten_data

    def reset_flattened_data(self, endpoint: str):
        """
        Resets the flattened data and metadata with a new endpoint.

        Parameters:
        :param endpoint: The new endpoint URL.
        :type endpoint: str
        """
        self.metadata = {
            "Endpoint": endpoint,
            "DateRetrieved": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            + "Z",
            "Accuracy": -1.0,
        }
        self.prac_role_obj = self.prac_loc_obj = []
        self.prac_obj = None
        self.flatten_data = {}


class StandardProcessModel(BaseModel):
    """
    A Pydantic model representing structured data for healthcare practitioners, their roles, and locations,
    including metadata about data retrieval. This model serves as a standardized schema for serializing
    FHIR resources into a consistent and validated format, facilitating the processing and usage of healthcare information.

    Attributes:
        Endpoint (Optional[str]): The source endpoint from where the data was retrieved.
        DateRetrieved (Optional[datetime]): The timestamp when the data was retrieved.
        AccuracyScore (Optional[float]): An accuracy score assessing the quality or reliability of the data.
    """

    # Model metadata
    Endpoint: Optional[str] = None
    DateRetrieved: Optional[str] = None
    Accuracy: Optional[float] = None

    # Practitioner fields
    FullName: Optional[str] = None
    NPI: Optional[int] = None
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Gender: Optional[str] = None
    LastPracUpdate: Optional[str] = None

    # Practitioner role fields
    GroupName: Optional[str] = None
    Taxonomy: Optional[str] = None
    LastPracRoleUpdate: Optional[str] = None

    # Location fields
    ADD1: Optional[str] = None
    ADD2: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[str] = None
    Phone: Optional[int] = None
    Fax: Optional[int] = None
    Email: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    LastLocationUpdate: Optional[str] = None

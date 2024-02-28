import re
from pydantic import BaseModel
from datetime import datetime

# from fhirtypepkg.fhirtype import ExceptionNPI
from fhirclient.models.domainresource import DomainResource
from typing import Optional
from typing import List, Dict, Any


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
    # m = re.match(r"([0-9]{10})", npi)
    #
    # if m is None:
    #     raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")
    # else:
    #     valid_npi = m.group(0)
    #
    # if valid_npi is None:
    #     raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")
    #
    # return m.group(0)
    return npi


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


# "name": [
#   {
#     "family": "Dykstra",
#     "given": [
#       "Michelle L"
#     ],
#     "text": "Michelle L Dykstra, PhD"
#   }
# ],
def get_name(resource, sub_attr: str = None):
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
            return re.split(r"[^a-zA-Z]", name_obj.given[0])[0].capitalize() if name_obj.given else None
        elif sub_attr == "last":
            # Split by anything other than a letter
            return (
                    name_obj.family.capitalize() or None
            )
    return None


def get_npi(resource):
    if hasattr(resource, "identifier"):
        field_value = getattr(resource, "identifier", [])
        if field_value is None:
            return None
        for identifier in field_value:
            if identifier.system == "http://hl7.org/fhir/sid/us-npi":
                return validate_npi(identifier.value)
    return None


def get_taxonomy(qualification_obj):
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
    name = None
    if resource.organization and hasattr(resource.organization, "name"):
        name = resource.organization.name
        name = name.replace("_", " ")

    return name


def flatten_prac(resource: DomainResource):
    gender = resource.gender.capitalize() if resource.gender else None
    last_update = (
        resource.meta.lastUpdated.isostring if resource.meta.lastUpdated else None
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
    last_update = (
        resource.meta.lastUpdated.isostring if resource.meta.lastUpdated else None
    )

    org_name = get_org_name(resource=resource)

    return {
        "GroupName": org_name,
        "Taxonomy": get_role_taxonomy(resource),
        "LastPracRoleUpdate": last_update
    }


def flatten_loc(resource: DomainResource):
    add1, city, state, zip_code = get_loc_address(resource)
    phone, fax, email = get_loc_telecom(resource)
    lat, lng = get_loc_coordinates(resource)
    last_update = (
        resource.meta.lastUpdated.isostring if resource.meta.lastUpdated else None
    )
    return {
        "ADD1": add1,
        "ADD2": "Optional",
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


def transform_flatten_data(flatten_data):
    transformed_list = []

    # Iterate through the flatten_data list
    for entry in flatten_data:
        # Check if 'roles' key exists and has items
        if "roles" in entry and entry["roles"]:
            for role in entry["roles"]:
                # Extract role-specific fields here if needed
                role_specific_fields = {key: role[key] for key in role if key not in ['locations']}

                # Check if 'locations' key exists and has items
                if "locations" in role and role["locations"]:
                    for location in role["locations"]:
                        # Combine general practitioner info, role-specific info, and location info
                        combined_entry = {**entry, **role_specific_fields, **location}
                        # Remove 'roles' key as it's no longer needed in the combined view
                        combined_entry.pop('roles', None)
                        transformed_list.append(combined_entry)
                else:
                    # If there are no locations, still combine practitioner info with role-specific info
                    combined_entry = {**entry, **role_specific_fields}
                    combined_entry.pop('roles', None)
                    transformed_list.append(combined_entry)
        else:
            # If there are no roles, the entry is already in the correct format
            transformed_list.append(entry)

    return transformed_list


class FlattenSmartOnFHIRObject:
    """
    Deserializes SmartOnFHIR Objects into a structured JSON format.
    Stores flattened practitioner, role, and location data.
    """

    def __init__(self, endpoint: str) -> None:
        self.metadata = {
            "Endpoint": endpoint,
            "DateRetrieved": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "Accuracy": -1.0,
        }
        self.prac_obj = None
        self.prac_role_obj: List = []
        self.prac_loc_obj: List = []

        # Flatten related declarations
        self.flatten_prac = None
        self.flatten_prac_role: List = []
        self.flatten_prac_loc: List = []
        self.flatten_data: List[Dict[str, Any]] = []

    def flatten_all(self) -> None:
        """
        Processes and flattens FHIR Client objects for practitioners, their roles, and locations into structured data.
        """
        # Processing for practitioners with roles and locations
        if self.prac_loc_obj and self.prac_role_obj and self.prac_obj:
            # Check and append roles with locations
            if "roles" in self.flatten_data[-1]:
                for role, loc in zip(self.flatten_data[-1]["roles"], self.prac_loc_obj):
                    flat_loc = flatten_loc(resource=loc)
                    model_data = StandardProcessModel.Location(**flat_loc).model_dump()
                    role["locations"] = [model_data]

        # Processing for practitioners with roles but without locations
        elif self.prac_role_obj and self.prac_obj:
            if "roles" not in self.flatten_data[-1]:
                self.flatten_data[-1]["roles"] = []
            for role in self.prac_role_obj:
                flat_role = flatten_role(resource=role)
                model_data = StandardProcessModel.PractitionerRole(**flat_role).model_dump()
                self.flatten_data[-1]["roles"].append(model_data)

        # Processing for practitioners without roles or locations
        elif self.prac_obj:
            self.flatten_prac = flatten_prac(resource=self.prac_obj)
            model_data = StandardProcessModel.Practitioner(**self.flatten_prac).model_dump()
            self.flatten_data.append({**self.metadata, **model_data})

    def get_related_flat_data(self) -> List[Dict[str, Any]]:
        """
        Returns the flattened data.
        """
        return self.flatten_data

    def get_flattened_data(self) -> List[Dict[str, Any]]:
        """
        Returns the flattened data.
        """
        return transform_flatten_data(self.flatten_data)

    def reset_flattened_data(self):
        self.prac_role_obj = self.prac_loc_obj = self.flatten_data = []
        self.prac_obj = None


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
    DateRetrieved: Optional[datetime] = None
    AccuracyScore: Optional[float] = None

    class Practitioner(BaseModel):
        """
        Nested model for details about healthcare practitioners, including personal and professional information.
        """

        FullName: Optional[str] = None
        NPI: Optional[int] = None
        FirstName: Optional[str] = None
        LastName: Optional[str] = None
        Gender: Optional[str] = None
        LastPracUpdate: Optional[str] = None

    class PractitionerRole(BaseModel):
        """
        Nested model for representing the roles of healthcare practitioners.
        """

        GroupName: Optional[str] = None
        Taxonomy: Optional[str] = None
        LastPracRoleUpdate: Optional[str] = None

    class Location(BaseModel):
        """
        Nested model for healthcare locations, detailing both contact and geographic information.
        """

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

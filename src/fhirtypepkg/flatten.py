import json
import re
from pydantic import BaseModel
from datetime import datetime
from fhirtypepkg.fhirtype import ExceptionNPI
from fhirclient.models.domainresource import DomainResource


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


def get_name(name_obj, sub_attr: str = None):
    name_obj = name_obj[0]  # Assuming the first name object is the one we want
    if sub_attr == "full":
        full_name = name_obj.family or None
        given_names = ' '.join(name_obj.given) if name_obj.given else None
        if given_names:
            full_name += ', ' + given_names
        return full_name
    elif sub_attr == "first":
        return name_obj.family or None
    elif sub_attr == "last":
        return name_obj.given[0] if name_obj.given else None


def get_npi(identifier_obj):
    for identifier in identifier_obj:
        if identifier.system == "http://hl7.org/fhir/sid/us-npi":
            return identifier.value
        else:
            # if there is no npi, return -1 to not upset Pydantic class
            return -1


def get_taxonomy(qualification_obj):
    if qualification_obj is None:
        return "Taxonomy not found"
    for qualification in qualification_obj:
        for coding in qualification.code.coding:
            if coding.system == "http://nucc.org/provider-taxonomy":
                return coding.code
    return "Taxonomy not found"


def findValue(resource: DomainResource, attribute: str, sub_attr: str = None):
    try:
        # if attribute in resource:
        if hasattr(resource, attribute):
            field_value = getattr(resource, attribute, [])
            if attribute == "name":
                if sub_attr == "full":
                    return get_name(field_value, "full")
                elif sub_attr == "first":
                    return get_name(field_value, "first")
                elif sub_attr == "last":
                    return get_name(field_value, "last")
            elif attribute == "identifier":
                if sub_attr == "npi":
                    return get_npi(field_value)
            elif attribute == "gender":
                return resource.gender if resource.gender else None
            elif attribute == "qualification":
                if sub_attr == "taxonomy":
                    return get_taxonomy(field_value)
        return "NO FIELD NAME BUDDY?"
    except AttributeError:
        print("this is in exception case")
        return "IDK BUDDY"


def flatten(resource: DomainResource, client: str):
    print("Client is :", client)
    sample_data = {
        "Endpoint": client,
        "DataRetrieved": datetime.now(),
        "FullName": findValue(resource, "name", sub_attr="full"),
        "NPI": findValue(resource, "identifier", sub_attr="npi"),
        "FirstName": findValue(resource, "name", sub_attr="first"),
        "LastName": findValue(resource, "name", sub_attr="last"),
        "Gender": findValue(resource, "gender"),
        "Taxonomy": findValue(resource, "qualification", sub_attr="taxonomy"),
        "GroupName": "GroupName_data",
        "ADD1": "ADD1_data",
        "ADD2": "ADD2_data",
        "City": "City_data",
        "State": "State_data",
        "Zip": 97331,
        "Phone": 123412,
        "Fax": 12312312,
        "Email": "Email_data",
        "lat": 1.12312,
        "lng": 20.123,
        "LastPracUpdate": datetime.now(),
        "LastPracRoleUpdate": datetime.now(),
        "LastLocationUpdate": datetime.now(),
        "AccuracyScore": 10.0
    }

    user = Process(**sample_data)

    # print(user.model_dump_json(indent=4))
    return user.model_dump()


class Process(BaseModel):
    Endpoint: str
    DataRetrieved: datetime | None  # Add the type annotation here
    FullName: str
    NPI: int
    FirstName: str
    LastName: str
    Gender: str
    Taxonomy: str | int
    GroupName: str
    ADD1: str
    ADD2: str
    City: str
    State: str
    Zip: int
    Phone: int
    Fax: int
    Email: str
    lat: float
    lng: float
    LastPracUpdate: datetime
    LastPracRoleUpdate: datetime
    LastLocationUpdate: datetime
    AccuracyScore: float

    # Add a method to update the model from a FHIR resource
    def update_from_fhir(self, resource: DomainResource):
        for field in self.__fields__:
            fhir_value = self.get_fhir_value(resource, field)
            if fhir_value is not None:
                setattr(self, field, fhir_value)

    @staticmethod
    def get_fhir_value(resource: DomainResource, field_name: str):
        # This is a simple example, you'll need to expand this logic
        # to handle your specific FHIR structure and fields.
        # You may also need to handle nested structures.
        try:
            # Direct mapping, if the attribute exists directly on the resource
            return getattr(resource, field_name)
        except AttributeError:
            # Handle nested structures or provide defaults
            # Example for nested 'name' field, assuming it's a list of HumanName
            if field_name == 'FullName' and hasattr(resource, 'name'):
                names = getattr(resource, 'name', [])
                if names:
                    # Just an example, you might need to join given and family names
                    return ' '.join([n.given[0] + ' ' + n.family for n in names if n.given and n.family])
            return None  # or a default value


class Flatten:

    def __init__(self) -> None:
        self.DATA = None
        self.RESOURCE = None
        pass

    def flattenResource(self, resource: DomainResource, client: str):
        # make a call to a function which will convert
        # the resource to required JSON format and call
        # the pydantic class Process
        data = flatten(resource=resource, client=client)
        self.RESOURCE = resource
        self.DATA = data
# print(user)

# print(user.model_dump())



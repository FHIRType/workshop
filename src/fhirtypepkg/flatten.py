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
        given_names = " ".join(name_obj.given) if name_obj.given else None
        if given_names:
            full_name += ", " + given_names
        return full_name
    elif sub_attr == "first":
        return name_obj.family or None
    elif sub_attr == "last":
        return name_obj.given[0] if name_obj.given else None


def get_npi(identifier_obj):
    if identifier_obj is None:
        return -1
    for identifier in identifier_obj:
        if identifier.system == "http://hl7.org/fhir/sid/us-npi":
            return validate_npi(identifier.value)
        else:
            return -1


def get_taxonomy(qualification_obj):
    if qualification_obj is None:
        return "Taxonomy not found"
    for qualification in qualification_obj:
        for coding in qualification.code.coding:
            if coding.system == "http://nucc.org/provider-taxonomy":
                return coding.code
    return "Taxonomy not found"


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
    return "NO ADDY BUDDY"


def get_telecom(telecom_obj, sub_attr: str = None):
    if telecom_obj is not None:
        for telecom in telecom_obj:
            if telecom.system == sub_attr:
                return telecom.value
    return "NO TELECOM"


def get_last_update(meta_obj):
    if meta_obj:
        return meta_obj.lastUpdated.isostring


def findValue(resource: DomainResource, attribute: str, sub_attr: str = None):
    try:
        if hasattr(resource, attribute):
            field_value = getattr(resource, attribute, [])
            if attribute == "name":
                return get_name(field_value, sub_attr=sub_attr)
            elif attribute == "identifier":
                if sub_attr == "npi":
                    return get_npi(field_value)
            elif attribute == "gender":
                return resource.gender if resource.gender else None
            elif attribute == "qualification":
                if sub_attr == "taxonomy":
                    return get_taxonomy(field_value)
            elif attribute == "address":
                return get_address(field_value, sub_attr=sub_attr)
            elif attribute == "telecom":
                return get_telecom(field_value, sub_attr=sub_attr)
            elif attribute == "meta":
                if sub_attr == "prac":
                    if resource.resource_type == "Practitioner":
                        return get_last_update(field_value)
                elif sub_attr == "role":
                    if resource.resource_type == "PractitionerRole":
                        return get_last_update(field_value)
                elif sub_attr == "location":
                    if resource.resource_type == "Location":
                        return get_last_update(field_value)
                return "N/A"
        return "Your attribute key is WRONG, smh"
    except AttributeError:
        return "OH we in trouble BUDDY"


def flatten(resource: DomainResource, client: str):
    print("Client is :", client)
    flattened = {
        "Endpoint": client,
        "DataRetrieved": datetime.now(),
        "FullName": findValue(resource, "name", sub_attr="full"),
        "NPI": findValue(resource, "identifier", sub_attr="npi"),
        "FirstName": findValue(resource, "name", sub_attr="first"),
        "LastName": findValue(resource, "name", sub_attr="last"),
        "Gender": findValue(resource, "gender"),
        "Taxonomy": findValue(resource, "qualification", sub_attr="taxonomy"),
        "GroupName": "GroupName_data",
        "ADD1": findValue(resource, "address", sub_attr="street"),
        "ADD2": "ADD2_data",
        "City": findValue(resource, "address", sub_attr="city"),
        "State": findValue(resource, "address", sub_attr="state"),
        "Zip": findValue(resource, "address", sub_attr="zip"),
        "Phone": findValue(resource, "telecom", sub_attr="phone"),
        "Fax": findValue(resource, "telecom", sub_attr="fax"),
        "Email": findValue(resource, "telecom", sub_attr="email"),
        "lat": 0.0000,
        "lng": 0.0000,
        "LastPracUpdate": findValue(resource, "meta", sub_attr="prac"),
        "LastPracRoleUpdate": findValue(resource, "meta", sub_attr="role"),
        "LastLocationUpdate": findValue(resource, "meta", sub_attr="location"),
        "AccuracyScore": -1,
    }
    # Process through pydantic and return
    user = Process(**flattened)
    return user.model_dump()


class Flatten:
    def __init__(self) -> None:
        self.DATA = None
        self.RESOURCE = None

    def flattenResource(self, resource: DomainResource, client: str):
        data = flatten(resource=resource, client=client)
        self.RESOURCE = resource
        self.DATA = data


# Pydantic class
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
    Zip: str | int
    Phone: str
    Fax: str
    Email: str
    lat: float
    lng: float
    LastPracUpdate: str | datetime
    LastPracRoleUpdate: str | datetime
    LastLocationUpdate: str | datetime
    AccuracyScore: float

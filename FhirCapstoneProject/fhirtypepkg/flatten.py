import re
from pydantic import BaseModel
from datetime import datetime
# from fhirtypepkg.fhirtype import ExceptionNPI
from fhirclient.models.domainresource import DomainResource
from typing import Optional


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
    )

    return formatted_number


def get_name(name_obj, sub_attr: str = None):
    name_obj = name_obj[0]  # Assuming the first name object is the one we want
    if sub_attr == "full":
        full_name = name_obj.family or None
        given_names = " ".join(name_obj.given) if name_obj.given else None
        if given_names:
            full_name += ", " + given_names
        return full_name
    elif sub_attr == "first":
        return name_obj.family.capitalize() or None
    elif sub_attr == "last":
        # Split by anything other than a letter
        return re.split(r'[^a-zA-Z]', name_obj.given[0])[0].capitalize() if name_obj.given else None


def get_npi(identifier_obj):
    if identifier_obj is None:
        return None
    for identifier in identifier_obj:
        if identifier.system == "http://hl7.org/fhir/sid/us-npi":
            print("IM here for :", identifier.value)
            return validate_npi(identifier.value)
    return "NPI is in invalid format: " + identifier.value


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
                # return is_valid_taxonomy(coding.code) if 1 else "Invalid Taxonomy: " + coding.code
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


def get_telecom(telecom_obj, sub_attr: str = None):
    if telecom_obj is not None:
        for telecom in telecom_obj:
            if telecom.system == sub_attr:
                return telecom.value
    return None


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
                return resource.gender.capitalize() if resource.gender else None
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
                return None
        return "Invalid attribute key"
    except AttributeError:
        return "OH we in trouble BUDDY"


def flatten_prac(resource: DomainResource, endpoint: str):
    print("Client is :", endpoint)
    flattened_prac = {
        # "Endpoint": endpoint,
        # "DateRetrieved": datetime.utcnow(),
        "FullName": findValue(resource, "name", sub_attr="full"),
        "NPI": findValue(resource, "identifier", sub_attr="npi"),
        "FirstName": findValue(resource, "name", sub_attr="first"),
        "LastName": findValue(resource, "name", sub_attr="last"),
        "Gender": findValue(resource, "gender"),
        # "Taxonomy": findValue(resource, "qualification", sub_attr="taxonomy"),
        # "GroupName": "GroupName_data",
        # "ADD1": findValue(resource, "address", sub_attr="street"),
        # "ADD2": None,
        # "City": findValue(resource, "address", sub_attr="city"),
        # "State": findValue(resource, "address", sub_attr="state"),
        # "Zip": findValue(resource, "address", sub_attr="zip"),
        # "Phone": findValue(resource, "telecom", sub_attr="phone"),
        # "Fax": findValue(resource, "telecom", sub_attr="fax"),
        # "Email": findValue(resource, "telecom", sub_attr="email"),
        # "lat": None,
        # "lng": None,
        "LastPracUpdate": findValue(resource, "meta", sub_attr="prac"),
        # "LastPracRoleUpdate": findValue(resource, "meta", sub_attr="role"),
        # "LastLocationUpdate": findValue(resource, "meta", sub_attr="location"),
        # "AccuracyScore": None,
    }
    # Process through pydantic and return
    # user = StandardProcessModel(**flattened)
    return flattened_prac


def flatten_role():
    pass


def flatten_loc():
    pass


class FlattenSmartOnFHIRObject:
    """
    This class accepts SmartOnFHIR Object and deserializes it into JSON
    Method 1: reads type and stores relevant data somewhere (either as pydantic class or strings)
    method 2: returns the JSON representation of the Object
    Eventually: want it to output prac, role and location as a json string
    """

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.date_retrieved = datetime.utcnow()
        self.accuracy = -1.0

        # uses class members to store incoming FHIR class objects
        self.prac_obj = None
        self.prac_role_obj = []
        self.prac_loc_obj = []

        # these store flattened FHIR objects
        self.flatten_prac = None
        self.flatten_prac_role = []
        self.flatten_prac_loc = []

        # this is going to store our flatten
        self.flatten_data = [
            self.endpoint,
            self.date_retrieved,
            self.accuracy
        ]

    # def flatten_practitioner_object(self, prac_res: DomainResource):
    #     data = flatten_prac(resource=prac_res, endpoint=self.endpoint)
    #     self.prac_obj = data
    #
    # def flatten_practitioner_role_object(self, pracRole_res: DomainResource):
    #     data = flatten_role()
    #     self.prac_role_obj.append(data)
    #
    # def flatten_practitioner_loc_object(self, pracRole_res: DomainResource):
    #     data = flatten_loc()
    #     self.prac_role_obj.append(data)

    def flatten_all(self):
        """
        This method will deserialize FHIR Client objects into the StandardProcessModel (Pydantic)
        and append it into our flatten data list
        :return: void
        """
        self.flatten_prac = flatten_prac(resource=self.prac_obj, endpoint=self.endpoint)

        # role
        # for role in self.prac_role_obj:
        #     self.flatten_prac_role.append(
        #         flatten_role(resource=role, endpoint=self.endpoint)
        #     )
        #
        # # loc
        # for loc in self.prac_loc_obj:
        #     self.flatten_prac_loc.append(
        #         flatten_loc(resource=loc, endpoint=self.endpoint)
        #     )

    def build_models(self):
        # TODO: retain relationship between prac_role and prac_loc
        # user = StandardProcessModel(**flattened)
        # return user.model_dump()

        # call flatten_all first to build the models
        self.flatten_all()

        # case 1: we only have practitioner, no loc and role
        if self.flatten_prac and not (self.flatten_prac_loc and self.flatten_prac_role):
            # new_model = StandardProcessModel(**self.flatten_prac)
            print("IM IN HERE HELP")
            print(self.flatten_prac)
            new_model = StandardProcessModel.Practitioner(**self.flatten_prac)
            new_model = new_model.model_dump()
            self.flatten_data.append(new_model)

        # case 2: we have a prac and prac role but no loc
        if self.flatten_prac and self.flatten_prac_role and not self.flatten_prac_loc:
            new_model = StandardProcessModel(
                Endpoint=self.endpoint,
                DateRetrieved="None",
                FullName="None",
                NPI="None",
                FirstName="None",
                LastName="None",
                Gender="None",
                Taxonomy="None",
                LastPracRoleUpdate="None"
            )
            new_model = new_model.model_dump()
            self.flatten_data.append(new_model)

        # case 3: we have all three
        if self.flatten_prac and self.flatten_prac_role and self.flatten_prac_loc:
            # make new object and pass them to the Pydantic model
            new_model = StandardProcessModel(
                **self.flatten_prac
            )
            new_model = new_model.model_dump()
            self.flatten_data.append(new_model)

    def get_flatten_data(self):
        return self.flatten_data


# flatten them all and stuff them into the list in Flatten
# shove the data form each one into discrete Pydantic models
# deserialize the model into dict and append into our self.Flatten data list


# Pydantic class
class StandardProcessModel(BaseModel):
    """

    """
    # Model metadata
    Endpoint: Optional[str]
    DateRetrieved: Optional[datetime]
    AccuracyScore: Optional[float]

    class Practitioner(BaseModel):
        FullName: Optional[str]
        NPI: Optional[str]
        FirstName: Optional[str]
        LastName: Optional[str]
        Gender: Optional[str]
        LastPracUpdate: Optional[str] = None

    class PractitionerRole(BaseModel):
        Taxonomy: Optional[str]
        LastPracRoleUpdate: Optional[str] = None

    class Location(BaseModel):
        GroupName: Optional[str]
        ADD1: Optional[str]
        ADD2: Optional[str] = None
        City: Optional[str]
        State: Optional[str]
        Zip: Optional[str]
        Phone: Optional[str]
        Fax: Optional[str]
        Email: Optional[str]
        lat: Optional[float]
        lng: Optional[float]
        LastLocationUpdate: Optional[str] = None

    # # This is model metadata
    # Endpoint: Optional[str]
    # DateRetrieved: Optional[datetime]
    # AccuracyScore: Optional[float]
    #
    # # This is practitioner data
    # FullName: Optional[str]
    # NPI: Optional[str]
    # FirstName: Optional[str]
    # LastName: Optional[str]
    # Gender: Optional[str]
    # LastPracUpdate: Optional[str | datetime] = None
    #
    # # This is practitioner role data
    # Taxonomy: Optional[str]
    # LastPracRoleUpdate: Optional[str | datetime] = None
    #
    # # This is location data
    # GroupName: Optional[str]
    # ADD1: Optional[str]
    # ADD2: Optional[str] = None
    # City: Optional[str]
    # State: Optional[str]
    # Zip: Optional[str]
    # Phone: Optional[str]
    # Fax: Optional[str]
    # Email: Optional[str]
    # lat: Optional[float]
    # lng: Optional[float]
    # LastLocationUpdate: Optional[str | datetime] = None

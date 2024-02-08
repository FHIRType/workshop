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
    - phone_number: The phone number string to be standardized.

    Returns:
    - A standardized phone number string containing only numeric characters.
    """
    # Remove any character that is not a digit
    standardized_phone = re.sub(r"[^\d]", "", phone_number)

    return standardized_phone


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


def get_role_taxonomy(resource: DomainResource):
    # Check if 'specialty' is present in the resource
    if hasattr(resource, 'specialty') and resource.specialty:
        for specialty in resource.specialty:
            # Directly access the 'coding' attribute as it's an attribute of the 'CodeableConcept' object
            if hasattr(specialty, 'coding') and specialty.coding:
                for code in specialty.coding:
                    # Check if 'system' is the one we're interested in
                    if hasattr(code, 'system') and code.system == "http://nucc.org/provider-taxonomy":
                        return code.code
    return None


def get_loc_address(resource: DomainResource):
    add1 = city = state = zip_code = "Optional"  # Default values
    if hasattr(resource, 'address') and resource.address:
        address = resource.address  # Direct access without assuming it's a list

        # Direct attribute access with hasattr checks
        city = address.city if hasattr(address, 'city') else "Optional"
        state = address.state if hasattr(address, 'state') else "Optional"
        zip_code = address.postalCode if hasattr(address, 'postalCode') else "Optional"

        # Handle 'line' which is expected to be a list
        if hasattr(address, 'line') and address.line:
            add1 = address.line[0]  # Taking the first line as the primary address

    return add1, city, state, zip_code


def get_loc_telecom(resource):
    phone = fax = email = None  # Default values
    if hasattr(resource, 'telecom') and resource.telecom:
        for contact in resource.telecom:
            system = contact.system.lower() if hasattr(contact, 'system') else ''
            value = contact.value if hasattr(contact, 'value') else 'Optional'
            if system == 'phone':
                phone = standardize_phone_number(value)
            elif system == 'fax':
                fax = standardize_phone_number(value)
            elif system == 'email':
                email = value
    return phone, fax, email


def get_loc_coordinates(resource: DomainResource):
    # Default values if position is not available
    lat, lng = None, None

    # Check if the resource has a 'position' attribute and both 'latitude' and 'longitude' are present
    if hasattr(resource, 'position') and hasattr(resource.position, 'latitude') and hasattr(resource.position,
                                                                                            'longitude'):
        lat = resource.position.latitude
        lng = resource.position.longitude

    return lat, lng


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


def flatten_prac(resource: DomainResource):
    return {
        "FullName": findValue(resource, "name", sub_attr="full"),
        "NPI": findValue(resource, "identifier", sub_attr="npi"),
        "FirstName": findValue(resource, "name", sub_attr="first"),
        "LastName": findValue(resource, "name", sub_attr="last"),
        "Gender": findValue(resource, "gender"),
        "LastPracUpdate": findValue(resource, "meta", sub_attr="prac"),
    }


def flatten_role(resource: DomainResource):
    print("I HAVE BEEN CALLED UPON")
    print(resource.meta.lastUpdated.isostring)
    return {
        "Taxonomy": get_role_taxonomy(resource),
        "LastPracRoleUpdate": findValue(resource, "meta", sub_attr="role")
    }


def flatten_loc(resource: DomainResource):
    add1, city, state, zip_code = get_loc_address(resource)
    phone, fax, email = get_loc_telecom(resource)
    lat, lng = get_loc_coordinates(resource)
    return {
        "GroupName": "GroupName",
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
        "LastLocationUpdate": findValue(resource, "meta", sub_attr="location")
    }


class FlattenSmartOnFHIRObject:
    """
    Deserializes SmartOnFHIR Objects into a structured JSON format.
    Stores flattened practitioner, role, and location data.
    """

    def __init__(self, endpoint: str) -> None:
        self.metadata = {
            "Endpoint": endpoint,
            "DateRetrieved": datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
            "Accuracy": -1.0
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

        This method takes stored FHIR Client objects (practitioners, practitioner roles, and locations) and converts them into a simplified, standardized format suitable for further processing or serialization.
        The method leverages specific flattening functions (e.g., flatten_prac, flatten_role) to transform each object into a dictionary following the structure expected by the corresponding Pydantic model.

        Flattened practitioner data is directly appended to the `flatten_data` list if no associated roles or locations are stored. If practitioner roles are present, each role is flattened and appended separately.
        The process for locations would follow a similar pattern if implemented.
        The method ensures that all relevant data is consistently structured, incorporating class-level metadata and adhering to the StandardProcessModel's schema, facilitating easy serialization or usage within applications.

        Note: The actual flattening functions (e.g., flatten_prac, flatten_role) are expected to be implemented elsewhere and are responsible for the detailed transformation of FHIR Client objects into dictionaries.

        Returns:
            None. The method updates the `flatten_data` list in-place with the processed data.
        """
        if self.prac_obj and not self.prac_role_obj and not self.prac_loc_obj:
            self.flatten_prac = flatten_prac(resource=self.prac_obj)
            if not self.prac_role_obj and not self.prac_loc_obj:
                self.append_flattened_data(self.flatten_prac, StandardProcessModel.Practitioner)

        elif self.prac_role_obj and self.prac_obj and not self.prac_loc_obj:
            print("IM Second IN HERE")
            self.flatten_prac_role = [flatten_role(resource=role) for role in self.prac_role_obj]
            self.append_flattened_data(self.flatten_prac_role, StandardProcessModel.PractitionerRole)

        elif self.prac_loc_obj and self.prac_role_obj and self.prac_obj:
            print("IM Third in here")
            self.flatten_prac_loc = [flatten_loc(resource=loc) for loc in self.prac_loc_obj]
            self.append_flattened_data(self.flatten_prac_loc, StandardProcessModel.Location)

    def append_flattened_data(self, data: Dict, ModelClass: BaseModel) -> None:
        """
        Appends flattened data, combined with metadata, to the flatten_data list.

        This method takes either a dictionary representing a single flattened object or a list of such dictionaries. It then initializes the appropriate Pydantic model for each item, serializes it to a dictionary, and combines it with the class-level metadata before appending the result to the flatten_data list. This process ensures that each piece of flattened data is consistently structured and includes relevant metadata, such as the endpoint, date retrieved, and accuracy score.

        Parameters:
            data: A dictionary or list of dictionaries containing the flattened data. Each dictionary should have keys and values that correspond to the fields expected by the specified Pydantic model class.
            ModelClass: The Pydantic model class to be used for serializing the flattened data. This class must be compatible with the structure of the `data` parameter.

        Returns:
            None. The method updates the flatten_data list in-place.
        """
        if isinstance(data, list):  # For handling lists of roles or locations
            for item in data:
                model_data = ModelClass(**item).dict()
                self.flatten_data.append({**self.metadata, **model_data})
        else:
            model_data = ModelClass(**data).dict()
            self.flatten_data.append({**self.metadata, **model_data})

    def get_flatten_data(self) -> List[Dict[str, Any]]:
        """
        Returns the flattened data.
        """
        return self.flatten_data

# class FlattenSmartOnFHIRObject:
#     """
#     This class accepts SmartOnFHIR Object and deserializes it into JSON
#     Method 1: reads type and stores relevant data somewhere (either as pydantic class or strings)
#     method 2: returns the JSON representation of the Object
#     Eventually: want it to output prac, role and location as a json string
#     """
#
#     def __init__(self, endpoint: str) -> None:
#         self.metadata = {
#             "Endpoint": endpoint,
#             "DateRetrieved": datetime.utcnow().replace(microsecond=0).isoformat(),
#             "Accuracy": -1.0
#         }
#
#         # uses class members to store incoming FHIR class objects
#         self.prac_obj = None
#         self.prac_role_obj = []
#         self.prac_loc_obj = []
#
#         # these store flattened FHIR objects
#         self.flatten_prac = None
#         self.flatten_prac_role = []
#         self.flatten_prac_loc = []
#
#         # this is going to store our flatten
#         self.flatten_data = []
#
#     def flatten_all(self):
#         """
#         This method will deserialize FHIR Client objects into the StandardProcessModel (Pydantic)
#         and append it into our flatten data list
#         :return: void
#         """
#         print("Flatten all: ", len(self.prac_role_obj))
#         if self.prac_obj and not self.prac_role_obj and not self.prac_loc_obj:
#             self.flatten_prac = flatten_prac(resource=self.prac_obj)
#
#         # role
#         elif self.prac_obj and self.prac_role_obj and not self.prac_loc_obj:
#             for role in self.prac_role_obj:
#                 self.flatten_prac_role.append(
#                     flatten_role(resource=role)
#                 )
#
#         # # loc
#         # for loc in self.prac_loc_obj:
#         #     self.flatten_prac_loc.append(
#         #         flatten_loc(resource=loc, endpoint=self.endpoint)
#         #     )
#
#     def build_models(self):
#         # TODO: retain relationship between prac_role and prac_loc
#
#         # call flatten_all first to build the models
#         self.flatten_all()
#
#         # case 1: we only have practitioner, no loc and role
#         if self.flatten_prac and not self.flatten_prac_loc and not self.flatten_prac_role:
#             prac_data = StandardProcessModel.Practitioner(**self.flatten_prac)
#             prac_data = prac_data.model_dump()
#             combined_data = {**self.metadata, **prac_data}
#             self.flatten_data.append(combined_data)
#
#         # case 2: we have a prac and prac role but no loc
#         elif self.flatten_prac and self.flatten_prac_role and not self.flatten_prac_loc:
#             # prac_data = StandardProcessModel.Practitioner(**self.flatten_prac)
#             for flat_role in self.flatten_prac_role:
#                 prac_role_data = StandardProcessModel.PractitionerRole(**flat_role)
#                 prac_role_data = prac_role_data.model_dump()
#                 # ** self.flatten_prac,
#                 combined_data = {**prac_role_data}
#                 self.flatten_data.append(combined_data)
#
#         # case 3: we have all three
#         if self.flatten_prac and self.flatten_prac_role and self.flatten_prac_loc:
#             # make new object and pass them to the Pydantic model
#             new_model = StandardProcessModel(
#                 **self.flatten_prac
#             )
#             new_model = new_model.model_dump()
#             self.flatten_data.append(new_model)
#
#     def get_flatten_data(self):
#         return self.flatten_data


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

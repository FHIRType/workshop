# Author: Trenton Young
# Date: 16 October 2023
# Description: Remote API endpoints and helpful functionality for querying and parsing their data.


_PRACTITIONER = "Practitioner"
_PRACTITIONER_ROLE = "PractitionerRole"
_LOCATION = "Location"
_ORGANIZATION = "Organization"


class Endpoint:
    def __init__(
        self,
        name,
        host,
        address,
        enable_http=True,
        use_http_client=False,
        get_metadata_on_init=True,
        secure_connection_needed=True,
        id_prefix=None,
    ):
        self.name = name
        self.host = host
        self.address = address
        self.enable_http = enable_http
        self.use_http_client = use_http_client
        self.get_metadata_on_init = get_metadata_on_init
        self.secure_connection_needed = secure_connection_needed

        self.id_prefix = id_prefix

        self.resourceType = {
            _PRACTITIONER: _PRACTITIONER,
            _PRACTITIONER_ROLE: _PRACTITIONER_ROLE,
            _LOCATION: _LOCATION,
            _ORGANIZATION: _ORGANIZATION,
        }

        self.standardize = {
            # _PRACTITIONER+"_name": lambda input_str: input_str,
            # _LOCATION+"_phone_number": lambda input_str: input_str
        }

    def __str__(self):
        return (
            f"{self.name} ({self.host}{self.address})\n"
            f"- {_PRACTITIONER}: {self.resourceType.get(_PRACTITIONER)}\n"
            f"- {_PRACTITIONER_ROLE}: {self.resourceType.get(_PRACTITIONER_ROLE)}\n"
            f"- {_LOCATION}: {self.resourceType.get(_LOCATION)}\n"
            f"- {_ORGANIZATION}: {self.resourceType.get(_ORGANIZATION)}"
        )

    def print_info(self):
        print(
            "Name ",
            self.name,
            "host ",
            self.host,
            "address ",
            self.address,
            "ssl ",
            self.secure_connection_needed,
            "\n",
        )

    def set_standardization(self, mask_key, mask_function):
        self.standardize[mask_key] = mask_function

    def use_standardization(self, mask_key, str_to_standardize):
        output = str_to_standardize
        if mask_key in self.standardize:
            output = self.standardize[mask_key](str_to_standardize)

        return output

    def get_url(self) -> str:
        """Returns the address of the endpoint to which requests are prepended.
        Example: https://www.endpoint.org/fhir_server/

        @return Fully qualified URL as a string.
        """
        url = "https" if self.secure_connection_needed else "http"
        url += "://"
        url += self.host
        url += self.address

        return url

    def get_name(self) -> str:
        """Returns the name of the endpoint as defined in the config file.

        @return Config-defined name as a string.
        """
        return self.name

    def set_practitioner_str(self, new):
        self.resourceType[_PRACTITIONER] = new

    def set_practitioner_role_str(self, new):
        self.resourceType[_PRACTITIONER_ROLE] = new

    def set_location_str(self, new):
        self.resourceType[_LOCATION] = new

    def set_organization_str(self, new):
        self.resourceType[_ORGANIZATION] = new

    def get_resource_type_str(self, resource_type):
        return self.resourceType[resource_type]

    def get_practitioner_str(self):
        return self.resourceType[_PRACTITIONER]

    def get_practitioner_role_str(self):
        return self.resourceType[_PRACTITIONER_ROLE]

    def get_location_str(self):
        return self.resourceType[_LOCATION]

    def get_organization_str(self):
        return self.resourceType[_ORGANIZATION]

    def print_masks(self):
        for i in self.standardize:
            print("----> ", i, ": ", self.standardize[i])

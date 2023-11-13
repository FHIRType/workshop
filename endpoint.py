# Author: Trenton Young
# Date: 16 October 2023
# Description: Remote API endpoints and helpful functionality for querying and parsing their data.


_PRACTITIONER = "Practitioner"
_PRACTITIONER_ROLE = "PractitionerRole"
_LOCATION = "Location"
_ORGANIZATION = "Organization"


class Endpoint:
    def __init__(self, name, host, address, ssl=True):
        self.name = name
        self.host = host
        self.address = address
        self.ssl = ssl

        self.resourceType = {
            _PRACTITIONER: _PRACTITIONER,
            _PRACTITIONER_ROLE: _PRACTITIONER_ROLE,
            _LOCATION: _LOCATION,
            _ORGANIZATION: _ORGANIZATION
        }

        self.masks = {
            # _PRACTITIONER+"_name": lambda input_str: input_str,
            # _LOCATION+"_phone_number": lambda input_str: input_str
        }

    def __str__(self):
        return f"{self.name} ({self.host}{self.address})\n" \
               f"- {_PRACTITIONER}: {self.resourceType.get(_PRACTITIONER)}\n" \
               f"- {_PRACTITIONER_ROLE}: {self.resourceType.get(_PRACTITIONER_ROLE)}\n" \
               f"- {_LOCATION}: {self.resourceType.get(_LOCATION)}\n" \
               f"- {_ORGANIZATION}: {self.resourceType.get(_ORGANIZATION)}"

    def set_mask(self, mask_key, mask_function):
        self.masks[mask_key] = mask_function

    def use_mask(self, mask_key, str_to_standardize):
        output = str_to_standardize
        if mask_key in self.masks:
            output = self.masks[mask_key](str_to_standardize)

        return output

    def get_endpoint_url(self):
        url = "https" if self.ssl else "http"
        url += "://"
        url += self.host
        url += self.address

        return url

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

    def get_practitioner_role(self):
        return self.resourceType[_PRACTITIONER_ROLE]

    def get_location_str(self):
        return self.resourceType[_LOCATION]

    def get_organization_str(self):
        return self.resourceType[_ORGANIZATION]

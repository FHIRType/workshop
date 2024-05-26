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
        can_search_by_npi=False,
        secure_connection_needed=True,
        id_prefix=None,
    ):
        self.name = name
        self.host = host
        self.address = address
        self.enable_http = enable_http
        self.use_http_client = use_http_client
        self.get_metadata_on_init = get_metadata_on_init
        self.can_search_by_npi = can_search_by_npi
        self.secure_connection_needed = secure_connection_needed

        self.id_prefix = id_prefix

        self.resourceType = {
            _PRACTITIONER: _PRACTITIONER,
            _PRACTITIONER_ROLE: _PRACTITIONER_ROLE,
            _LOCATION: _LOCATION,
            _ORGANIZATION: _ORGANIZATION,
        }

    def __str__(self):
        return (
            f"{self.name} ({self.host}{self.address})\n"
            f"- {_PRACTITIONER}: {self.resourceType.get(_PRACTITIONER)}\n"
            f"- {_PRACTITIONER_ROLE}: {self.resourceType.get(_PRACTITIONER_ROLE)}\n"
            f"- {_LOCATION}: {self.resourceType.get(_LOCATION)}\n"
            f"- {_ORGANIZATION}: {self.resourceType.get(_ORGANIZATION)}"
        )

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

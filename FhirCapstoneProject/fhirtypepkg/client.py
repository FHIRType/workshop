# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Functionality to connect to and interact with Endpoints.
import email
import ssl
import json
import subprocess

import requests
import requests.adapters
import http.client
import time
from typing import Any
import fhirclient.models.bundle
from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
from fhirclient.models.domainresource import DomainResource
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.capabilitystatement import CapabilityStatement
from requests.exceptions import SSLError
from requests.exceptions import HTTPError

import FhirCapstoneProject.fhirtypepkg as fhirtypepkg
from FhirCapstoneProject.fhirtypepkg.fhirtype import ExceptionNPI
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.fhirtype import fhir_logger
from FhirCapstoneProject.fhirtypepkg.flatten import (
    FlattenSmartOnFHIRObject,
    validate_npi,
)


class FakeFilePointer:
    def __init__(self, content: bytes or str):
        self.content = content

    def readline(self, size: int or None = None) -> bytes or str:
        return self.content

    def close(self):
        pass

class FakeSocket:
    def __init__(self, curl_response: bytes):
        self.curl_response = curl_response

        # Split the headers and payload
        self.header, self.body = self.curl_response.split(b'\r\n\r\n')

        # Parse the header
        self.header = self.header.decode('utf-8')
        self.headers = self.header.split('\r\n')

        # Decode the output and parse it as JSON
        self.response_data = json.loads(self.body.decode('utf-8'))  # TODO this looks just like the other thing

    def makefile(self, mode: str, *args, **kwargs):
        binary = 'b' in mode

        if binary:
            return FakeFilePointer(self.curl_response)
        else:
            return FakeFilePointer(self.curl_response.decode('utf-8'))

    def get_body(self):
        return self.body

    def get_http_version(self):
        http_string = self.headers[0].split(' ')[0]

        if http_string == 'HTTP/1.1':
            return 11

        return http_string

    def get_status_code(self):
        return int(self.headers[0].split(' ')[1])

    def get_reason(self):
        return self.headers[0].split(' ', 2)[2]


class FakeHTTPResponse(http.client.HTTPResponse):
    def __init__(self, socket: FakeSocket):
        http.client.HTTPResponse.__init__(self, socket)
        self.socket = socket

        self.chunk_left = None
        self.chunked = True
        self.code = socket.get_status_code()
        self.status = socket.get_status_code()
        self.reason = socket.get_reason()
        self.version = socket.get_http_version()
        self._content = socket.body

        header_builder = email.message.Message()
        _raw_headers = []
        for header in socket.headers[1:]:
            name, value = header.split(": ", 2)
            header_builder.set_param(param=name, value=value,
                                     header=name)
            _raw_headers.append((name, value))

        header_message = http.client.HTTPMessage(header_builder)

        # self.headers = header_message
        self.headers = _raw_headers
        self.msg = header_message
        self._ft_has_been_read = False

    def read(self, amount: int or None = None):
        if self._ft_has_been_read:
            return None

        self._ft_has_been_read = True
        return self.socket.get_body()



def resolve_reference(_smart, reference: fhirclient.models.fhirreference.FHIRReference):
    """
    :param _smart:
    :param reference:
    :return: JSON Object of the resolved reference (hint: __init__ DomainResource with this return)
    """
    reference = reference.reference

    if reference is None:
        raise TypeError("FHIRReference to None")

    # return reference.read_from(_smart.smart.server)
    return _smart.http_json_query(reference, [])


def http_build_search(parameters: dict) -> list:
    """
    Generates a list of 2-tuples from a dict of parameters, used for generating HTTP requests

    Example:
        {"name": "John Smith", "age": 23}
        # yields a URL like "site.com?name=John%20Smith&age=23"
    """
    output = []

    for key in parameters:
        if parameters[key] is not None:
            output.append((key, parameters[key]))

    return output


def http_build_search_practitioner(
    name_family: str, name_given: str, npi: str or None
) -> list:
    """
    Simply extends `::fhirtypepkg.client.http_build_search` to build a list of 2-tuples specifically for practitioners
    """
    return http_build_search(
        {
            "family": name_family,
            "given": name_given,
            "identifier": npi,
        }  # TODO: Localization
    )


def http_build_search_practitioner_role(practitioner: prac.Practitioner) -> list:
    """
    Simply extends `::fhirtypepkg.client.http_build_search` to build a list of 2-tuples specifically
    for practitioner roles
    """
    return http_build_search({"practitioner": practitioner.id})  # TODO: Localization


def fhir_build_search(resource: DomainResource, parameters: dict) -> FHIRSearch:
    """
    Builds an arbitrary search object for the given DomainResource (`Practitioner` or `Location` from the `fhirclient`
    package) using the given parameters.

    Does not validate parameters against the resource's model.

    :param resource: DomainResource (e.g. `fhirclient.models.practitioner.Practitioner`)
    :param parameters: A dict of valid parameters for that resource.
    :return: A search which can be performed against a client's server.
    """
    return resource.where(struct=parameters)


def fhir_build_search_practitioner(
    name_family: str, name_given: str, npi: str or None
) -> FHIRSearch:
    """
    Builds a search object for the DomainResource `Practitioner` from a name and NPI.
    Will perform a validation on the NPI.
    :param name_given: Given name, or first name, of the search
    :param name_family: Family name, or last name, of the search
    :param npi: [formatted 0000000000] National Physician Identifier
    :return: A search which can be performed against a client's server.
    """
    parameters = {"family": name_family, "given": name_given}  # TODO: Localization

    if npi is not None:
        try:
            parameters["identifier"] = validate_npi(npi)  # TODO: Localization
        except ExceptionNPI:
            pass

    return fhir_build_search(prac.Practitioner, parameters)


def fhir_build_search_practitioner_role(practitioner: prac.Practitioner) -> FHIRSearch:
    """
    Builds a search object for the DomainResource `PractitionerRole` from a valid `Practitioner` DomainResource,
    this search is intended to find the `PractitionerRoles` associated with that valid `Practitioner`.
    :param practitioner: A valid DomainResource `Practitioner`
    :return: A search which can be performed against a client's server.
    """
    parameters = {"practitioner": practitioner.id}  # TODO: Localization

    return fhir_build_search(prac_role.PractitionerRole, parameters)


class SmartClient:
    """
    Overview
    --------
    Client used to make requests to an API endpoint. Each instance represents an individual endpoint and abstracts
    the querying method from the user. This SmartClient may make queries via the Smart on FHIR library or an HTTP
    request depending on the state of the system.

    Upon initialization: GETs a capability statement from the endpoint to check versioning and other important
    metadata. This connection remains persistent and is monitored for the life of the SmartClient.

    Attributes
    -----------
    endpoint
        Holds the data for connecting to an API endpoint, generated from config file

    smart
        Smart on FHIR object, used to make queries

    http_session
        Persistent HTTP connection, used to make queries

    _http_session_confirmed
        Whenever an HTTP request is made, the status is checked and updated here
    """

    # def __init__(self, endpoint: Endpoint, enable_http=True, get_metadata=True):
    def __init__(self, endpoint: Endpoint):
        """
        Initializes a SmartClient for the given Endpoint. Assumes the Endpoint is properly initialized.

        :param endpoint: A valid Endpoint object
        :param get_metadata: Whether to perform `::fhirtypepkg.client.SmartClient.find_endpoint_metadata`
        upon instantiation, if set to false this can always be called later.
        """
        self._can_search_by_npi = True

        self.endpoint = endpoint

        # TODO: Fail gracefully when an endpoint is down
        self.smart = client.FHIRClient(
            settings={
                "app_id": fhirtypepkg.fhirtype.get_app_id(),  # TODO: Localization
                "api_base": endpoint.get_url(),  # TODO: Localization
            }
        )

        if self.endpoint.enable_http:
            self.http_session = requests.Session()
            self._http_session_confirmed = False
            self._initialize_http_session()
        else:
            self._http_session_confirmed = None
            fhir_logger().info(
                "NO HTTP Connection per config for endpoint %s (%s), using FHIR Client only.",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )

        self._enable_http_client = False
        self.http_client_list = []
        self.http_client_mutex = 0
        if self.endpoint.use_http_client:
            fhir_logger().info(
                "USE CLIENT.HTTP Connection per config for endpoint %s (%s), this will override use of the FHIR Client.",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )
            self._enable_http_client = True

        if self.endpoint.get_metadata_on_init:
            self.metadata = self.find_endpoint_metadata()
            self._search_params = {}

            rest_capability = self.metadata.rest[0]

            if rest_capability is not None:
                for domain_resource in rest_capability.resource:
                    search_params = domain_resource.searchParam
                    if search_params is not None:
                        self._search_params[domain_resource.profile] = []
                        for param in search_params:
                            self._search_params[domain_resource.profile].append(
                                param.name
                            )

            # TODO: Localization
            prac_params = self._search_params.get(
                "http://hl7.org/fhir/StructureDefinition/Practitioner", None
            )

            if prac_params is not None and "identifier" in prac_params:
                self._can_search_by_npi = True

        self.Flatten = FlattenSmartOnFHIRObject(self.get_endpoint_name())

    def get_http_client(self) -> http.client.HTTPSConnection:
        self.http_client_mutex += 1
        connection = http.client.HTTPSConnection(self.endpoint.host)
        self.http_client_list.append(connection)

        return connection

    def release_http_client(self):
        self.http_client_mutex -= 1
        if len(self.http_client_list) > 0 and self.http_client_mutex <= 0:
            for client in self.http_client_list:
                client.close()

            self.http_client_list = []

    def is_http_session_confirmed(self) -> bool or None:
        """
        Returns value of protected flag, this flag is updated any time an HTTP request is made
        """
        return self._http_session_confirmed

    def _initialize_http_session(self):
        """
        Creates an HTTP session for this SmartClient and attempts to verify the connection,
        handles any failures to connect and logs using `::fhirtypepkg.logging_fhir.FHIRLogger`
        """
        # self.http_session.auth = (None, None)  # TODO: Authentication as needed
        self.http_session.auth = ("", "")

        # TODO [Logging]: This whole block is a consideration for Logging
        try:
            # Initialize HTTP connection by collecting metadata
            response = self.http_session.get(self.endpoint.get_url() + "Practitioner")

            if 200 <= response.status_code < 400:
                self._http_session_confirmed = True
            # TODO: Specific handling may be necessary
            elif 400 <= response.status_code < 600:
                fhir_logger().error(
                    "ERROR Connecting to %s (%s).",
                    self.get_endpoint_name(),
                    self.get_endpoint_url(),
                    response.status_code,
                )
                raise response.raise_for_status()
            else:
                raise requests.RequestException(
                    response=response, request=response.request
                )

        # TODO: Handle exceptions appropriately
        except requests.RequestException as e:
            fhir_logger().error(
                f"Error making HTTP request, unhandled by status code check:", e
            )
        except ssl.SSLCertVerificationError as e:
            fhir_logger().error(f"SSLCertVerificationError:", e, exc_info=True)

        if self._http_session_confirmed is not None:
            if self._http_session_confirmed:
                fhir_logger().info(
                    "HTTP connection established to endpoint %s (%s).",
                    self.get_endpoint_name(),
                    self.get_endpoint_url(),
                )
            else:
                fhir_logger().error(
                    "HTTP connection to %s (%s) failed. Try again later.",
                    self.get_endpoint_name(),
                    self.get_endpoint_url(),
                )
        else:
            fhir_logger().info(
                "NO HTTP Connection requested to endpoint %s (%s), using FHIR Client only.",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )

    def get_endpoint_url(self) -> str:
        """
        Calls `::fhirtypepkg.endpoint.Endpoint.get_url` on the internal endpoint
        """
        return self.endpoint.get_url()

    def get_endpoint_name(self) -> str:
        """
        Calls `::fhirtypepkg.endpoint.Endpoint.get_name` on the internal endpoint
        """
        return self.endpoint.name

    def http_query(self, query: str, params: list) -> requests.Response:
        """
        Sends a query to the API via an HTTP GET request and returns the body string unchanged.
        Confirms the HTTP session upon successful response, will raise an exception and try to initialize if
        not confirmed when called.
        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A string, the body of the response
        """

        if self._http_session_confirmed is None and not self._enable_http_client:
            fhir_logger().error(
                "Attempted to make HTTP Query without HTTP Session nor HTTP.Client enabled on %s (%s).",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )
            raise HTTPError

        query_url = self.endpoint.get_url() + query
        response = None

        if self._enable_http_client:
            """
            Attempt the query using the HTTP Client
            """

            # Update query_url to contain the params
            query_url += "?"
            for param in params:
                query_url += param[0]
                query_url += "="
                query_url += param[1]
                query_url += "&"
            query_url = query_url[:-1]

            """
            This does not work for PS
            
            # Generate the request using HTTP Client
            conn = self.get_http_client()
            conn.request("GET", query_url, headers={})
            http_response = conn.getresponse()

            # This is a straight up terrible way to do this, but it needs to wait and I don't have callbacks
            # Start a little timeout for this wait
            start = time.time()
            timeout = 30 * 1000
            waiting_for_response = True

            while waiting_for_response:
                if time.time() - start > timeout:
                    waiting_for_response = False
                    http_response.status = 408  # Set the status to 408 if we timed out
                    fhir_logger().warning(
                        "Timed out while %s waiting for a response from %s (%s).",
                        self.get_endpoint_name(),
                        query_url,
                        query_url,
                    )

                if http_response.status is None or 200 <= http_response.status < 300:
                    waiting_for_response = False

            if http_response.status == 408:
                response.status_code = 408
            """

            # Generate an HTTP Response from a curl
            # Perform an OS level https request and store the output bytes
            output = subprocess.check_output(['curl', '--ca-native', '-s', '-D', '-', query_url])
            # Decode the output and parse it as JSON

            curl_wrapper = FakeSocket(output)
            curl_response = FakeHTTPResponse(curl_wrapper)

            request_parse = requests.PreparedRequest()
            request_parse.url = query_url


            adapter = requests.adapters.HTTPAdapter()
            response = adapter.build_response(request_parse, curl_response)

        else:
            """
            Attempt the query using the HTTP Session
            """
            # Checks HTTP session and attempts to reestablish if unsuccessful.
            if not self._http_session_confirmed:
                self._initialize_http_session()
                fhir_logger().exception("No HTTP Connection, try reestablishing")
                raise Exception("No HTTP Connection, reestablishing.")

            # Only include the params list if there are params to include, otherwise Requests gets mad
            if len(params) > 0:
                response = self.http_session.get(query_url, params=params)
            else:
                response = self.http_session.get(self.endpoint.get_url() + query)

        # Check the status
        if 200 <= response.status_code < 300:
            self._http_session_confirmed = True
        else:
            raise requests.RequestException(response=response, request=response.request)

        return response

    def http_json_query(self, query: str, params: list) -> dict:
        """
        Sends a query to the API via an HTTP GET request, accepts as json and deserializes.
        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A list, deserialized from json response
        """
        response = self.http_query(query, params=params)

        # Used to check the content type of the response, only accepts those types specified in fhirtype
        content_type = fhirtypepkg.fhirtype.parse_content_type_header(
            response.headers["content-type"]
        )

        output = json.loads(response.text)

        if self._enable_http_client:
            self.release_http_client()

        try:
            # If the response has a LOCATION or ORGANIZATION reference, resolve that to a DomainResources
            for h in range(len(output)):
                domain_resource = output[h]
                if hasattr(domain_resource, "location"):  # TODO: localization
                    if type(domain_resource.location) is list:
                        for i in range(len(domain_resource.location)):
                            output[h].location[i] = loc.Location(
                                resolve_reference(self, domain_resource.location[i])
                            )

                    elif (
                        type(domain_resource.location)
                        is fhirclient.models.fhirreference.FHIRReference
                    ):
                        output[h].location = loc.Location(
                            resolve_reference(self, domain_resource.location)
                        )

        except TypeError as e:
            fhir_logger().warning(
                "Caught a TypeError while resolving a reference, could have been a None reference. (%s)",
                e,
            )
        except KeyError:
            pass

        if fhirtypepkg.fhirtype.content_type_is_json(content_type):
            return output
        else:
            return {}

    def http_fhirjson_query(self, query: str, params: list) -> list:
        """
        Sends a query to the API via an HTTP GET request, parses to a list of FHIR Resources.
        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A list of FHIR Resources
        """
        res = self.http_json_query(query, params)

        # Try to initialize a bundle from the response (if the response is a bundle)
        is_bundle = True
        bundle = [None]
        try:
            bundle = fhirclient.models.bundle.Bundle(res)
        except:
            is_bundle = False

        # Parse each entry in the bundle to the appropriate FHIR Resource, this bundle may contain different Resources
        parsed = []
        if is_bundle:
            # Parse each entry in the bundle into a FHIR Resource, this bundle may contain different Resources
            if bundle and bundle.entry:
                for entry in bundle.entry:
                    if entry:
                        parsed.append(entry.resource)
        else:
            parsed = [res]

        try:
            # If the response has a LOCATION or ORGANIZATION reference, resolve that to a DomainResources
            for h in range(len(parsed)):
                domain_resource = parsed[h]
                if hasattr(domain_resource, "location"):  # TODO: localization
                    if type(domain_resource.location) is list:
                        for i in range(len(domain_resource.location)):
                            parsed[h].location[i] = loc.Location(
                                resolve_reference(self, domain_resource.location[i])
                            )

                    elif (
                        type(domain_resource.location)
                        is fhirclient.models.fhirreference.FHIRReference
                    ):
                        parsed[h].location = loc.Location(
                            resolve_reference(self, domain_resource.location)
                        )

        except TypeError as e:
            fhir_logger().warning(
                "Caught a TypeError while resolving a reference, could have been a None reference. (%s)",
                e,
            )

        return parsed

    def fhir_query(self, search: FHIRSearch, resolve_references=True) -> list:
        """
        Returns the results of a search performed against this SmartClient's server
        :type search: FHIRSearch
        :param search: Arbitrary search, see `build_search`
        :rtype: list
        :return: Results of the search
        """
        output = None

        # TODO [Logging]: This whole block is a consideration for Logging
        try:
            output = search.perform_resources(self.smart.server)
        except FHIRValidationError as e:
            fhir_logger().exception(
                f"## FHIRValidationError: {e}"
            )  # TODO: Need to understand this exception
        except HTTPError as e:
            fhir_logger().exception(
                f"## HTTPError: {e}"
            )  # TODO: Probably need to notify and maybe trigger reconnect here
        except SSLError as e:
            fhir_logger().exception(
                f"## SSLError: {e}"
            )  # TODO: Probably need to notify and maybe trigger reconnect here

        if resolve_references:
            try:
                # If the response has a LOCATION or ORGANIZATION reference, resolve that to a DomainResources
                for h in range(len(output)):
                    domain_resource = output[h]
                    if hasattr(domain_resource, "location"):  # TODO: localization
                        if type(domain_resource.location) is list:
                            for i in range(len(domain_resource.location)):
                                output[h].location[i] = loc.Location(
                                    resolve_reference(self, domain_resource.location[i])
                                )

                        elif (
                            type(domain_resource.location)
                            is fhirclient.models.fhirreference.FHIRReference
                        ):
                            output[h].location = loc.Location(
                                resolve_reference(self, domain_resource.location)
                            )

            except TypeError as e:
                fhir_logger().warning(
                    "Caught a TypeError while resolving a reference, could have been a None reference. (%s)",
                    e,
                )

        return output

    def http_query_practitioner(
        self, name_family: str, name_given: str, npi: str
    ) -> list:
        """
        Generates a search with the given parameters and performs it against this SmartClient's HTTP session
            Note: Searching by NPI may take additional time as not all endpoints include it as a primary key.
        :param name_given: Given name, or first name, of the search
        :param name_family: Family name, or last name, of the search
        :param npi: [formatted 0000000000] National Physician Identifier
        :rtype: list
        :return: Results of the search
        """
        if self._can_search_by_npi:
            search = http_build_search_practitioner(name_family, name_given, npi)
        else:
            search = http_build_search_practitioner(name_family, name_given, None)

        return self.http_fhirjson_query("Practitioner", search)

    def fhir_query_practitioner(
        self,
        name_family: str,
        name_given: str,
        npi: str or None,
        resolve_references=True,
    ) -> list:
        """
        Generates a search with the given parameters and performs it against this SmartClient's server. If this
        SmartClient's endpoint does not support searching by identifier, the search will be performed with the
        given and family names only.
            Note: Searching by NPI may take additional time as not all endpoints include it as a primary key.
        :param name_given: Given name, or first name, of the search
        :param name_family: Family name, or last name, of the search
        :param npi: [formatted 0000000000] National Physician Identifier
        :rtype: list
        :return: Results of the search
        """

        if self._can_search_by_npi:
            output = self.fhir_query(
                fhir_build_search_practitioner(name_family, name_given, npi),
                resolve_references,
            )
        else:
            output = self.fhir_query(
                fhir_build_search_practitioner(name_family, name_given, None),
                resolve_references,
            )

        return output

    def http_query_practitioner_role(self, practitioner: prac.Practitioner) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner via HTTP session
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self.http_fhirjson_query(
            "PractitionerRole",
            http_build_search_practitioner_role(practitioner),  # TODO: Localization
        )

    def fhir_query_practitioner_role(
        self, practitioner: prac.Practitioner, resolve_references=False
    ) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner via Smart on FHIR client
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self.fhir_query(
            fhir_build_search_practitioner_role(practitioner), resolve_references
        )  # TODO need to trace this down

    def find_endpoint_metadata(self) -> CapabilityStatement:
        """
        Queries the remote endpoint via HTTP session for the endpoint's metadata (or "Capability Statement")
        :return: The Capability Statement parsed into a Smart on FHIR object
        """
        # TODO: Track down and understand PacificSource's metadata
        capability_via_fhir = self.smart.server.request_json(path="metadata")

        # capability_via_http = self.http_fhirjson_query(
        #     "metadata", []
        # )  # TODO: Localization

        # return None
        return CapabilityStatement(capability_via_fhir)

    def find_practitioner(
        self,
        name_family: str,
        name_given: str,
        npi: str or None,
        resolve_references=True,
    ) -> tuple[list[DomainResource], list[dict]]:
        """
        Searches for practitioners by first name, last name, and NPI (National Provider Identifier).

        This function first queries the FHIR Client unless the endpoint was configured to use the HTTP Client (which takes priority if it is enabled) by first name and last name, then checks the NPI of the returned practitioners.
        If a practitioner's NPI matches the provided NPI, the function returns a list containing a single practitioner object and a dictionary of standardized practitioner data.

        The practitioner data is standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.


        Parameters:
        :param resolve_references:
        :param name_given: The first name of the practitioner.
        :type name_given: string
        :param name_family: The last name of the practitioner.
        :type name_family: string
        :param npi: The National Provider Identifier of the practitioner.
        :type npi: string

        Returns:
        :rtype: tuple(list, list)
        :return tuple: A tuple containing two elements:
                - list: A list of practitioners (as FHIR resources) that match the first name and last name. If a practitioner also matches the NPI, the list will contain only that practitioner.
                - list: A list of dictionaries of standardized data for the practitioner that matches the NPI. If no practitioner matches the NPI, an empty dictionary is returned.
        """
        if not npi or len(npi) < 10:
            raise ValueError(
                f"Error npi not correct for search parameters value: {npi}"
            )

        # When the HTTP Client is enabled, this means that certain overrides need to happen,
        # so we use that over fhirclient
        if self._enable_http_client:
            practitioners_response = self.http_query_practitioner(
                name_family, name_given, npi
            )
        else:
            practitioners_response = self.fhir_query_practitioner(
                name_family, name_given, npi, resolve_references
            )

        prac_resources, filtered_prac = [], []
        unique_identifiers = set()

        if practitioners_response:
            for practitioner in practitioners_response:
                if practitioner.identifier:

                    for _id in practitioner.identifier:
                        if (
                            _id.system == "http://hl7.org/fhir/sid/us-npi"
                            and _id.value == npi
                        ):
                            if practitioner.id not in unique_identifiers:
                                print("im here\n\n\n\n\n")
                                self.Flatten.prac_obj = practitioner
                                unique_identifiers.add(practitioner.id)
                                # debug returns
                                prac_resources.append(practitioner)

        self.Flatten.flatten_all()
        return prac_resources, self.Flatten.get_flatten_data()

    def find_practitioner_role(
        self, practitioner: prac.Practitioner, resolve_references=False
    ) -> tuple[list[Any], list[Any]]:
        """
        Searches for and returns a list of roles associated with the given practitioner.

        This function queries the FHIR Client unless the endpoint was configured to use the HTTP Client (which takes priority if it is enabled) for roles associated with the practitioner passed in as a parameter.
        The roles are then standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.

        Note: The roles returned will only reflect those from the same endpoint as the practitioner was selected from.

        Parameters:
            resolve_references:
        :param practitioner: A Practitioner object for which to find associated roles.
        :type practitioner: fhirclient.models.practitioner.Practitioner

        Returns:
        :rtype: tuple(list, dict)
        :return tuple: A tuple containing two elements:
            - list: A list of practitioner roles (as FHIR resources) associated with the given practitioner.
            - dict: A dictionary of standardized data for the practitioner roles. If no roles are found, an empty dictionary is returned.
        """
        prac_roles, filtered_roles = [], []
        if self._enable_http_client:
            practitioner_roles_response = self.http_query_practitioner_role(
                practitioner
            )
        else:
            practitioner_roles_response = self.fhir_query_practitioner_role(
                practitioner, resolve_references
            )

        if not practitioner_roles_response:
            return [], []

        seen_roles = set()  # Track seen roles to avoid duplicates
        for role in practitioner_roles_response:
            if role.id not in seen_roles:
                seen_roles.add(role.id)
                self.Flatten.prac_role_obj.append(role)
                prac_roles.append(role)

        # self.Flatten.build_models()
        self.Flatten.flatten_all()
        return prac_roles, self.Flatten.get_flatten_data()

    def find_practitioner_role_locations(
        self, practitioner_role: prac_role.PractitionerRole
    ) -> tuple[list[Any], list[Any]]:
        """
        Searches for and returns a list of locations associated with a given practitioner role.

        This function queries the FHIR Client unless the endpoint was configured to use the HTTP Client (which takes priority if it is enabled) for locations associated with the practitioner role passed in as a parameter.
        Each location could represent a place where the practitioner works. For example, if Dr Alice Smith works at the hospital on 123 Main St using her cardiology role and at the clinic on 456 Main St using her neurology role, both locations would be returned.

        The locations are then standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.

        Parameters:
        :param practitioner_role: A PractitionerRole object for which to find associated locations.
        :type practitioner_role: fhirclient.models.practitionerrole.PractitionerRole

        Returns:
        :rtype: tuple(list, dict)
        :return tuple: A tuple containing two elements:
            - list: A list of locations (as FHIR resources) associated with the given practitioner role.
            - dict: A list of dictionaries of standardized data for the locations. If no locations are found, an empty list is returned.
        """
        locations, filtered_dictionary = [], []

        if not practitioner_role.location:
            raise ValueError(
                f"No location available in practitioner role for endpoint {self.get_endpoint_name()} prac-id: {practitioner_role.id}"
            )

        seen_loc = set()
        for role_location in practitioner_role.location:
            if role_location.id not in seen_loc:
                seen_loc.add(role_location.id)
                self.Flatten.prac_loc_obj.append(role_location)
                locations.append(role_location)

        self.Flatten.flatten_all()
        return locations, self.Flatten.get_flatten_data()

    def find_all_practitioner_data(
        self,
        name_family: str,
        name_given: str,
        npi: str or None,
        resolve_references=True,
    ):
        """
        Searches for and returns a list of practitioners and each role and location associated with them.

        Recursively calls each find_practitioner, find_practitioner_role, and find_practitioner_role_locations

        Parameters:
        :param name_given: The first name of the practitioner.
        :type name_given: string
        :param name_family: The last name of the practitioner.
        :type name_family: string
        :param npi: The National Provider Identifier of the practitioner.
        :type npi: string

        Returns:
        TODO : @HlaKarki help pls
        """
        practitioners, flatten = self.find_practitioner(
            name_family, name_given, npi, resolve_references
        )

        # TODO: Is there an intermediate acc model step here?

        practitioner_roles = []
        for prac in practitioners:
            practitioner_roles_response = self.find_practitioner_role(
                prac, resolve_references
            )

            for role in practitioner_roles_response:
                practitioner_roles.append(role)

        # practitioner_roles = self.find_practitioner_role(practitioners[0])

        practitioner_locations = []

        for role in practitioner_roles[0]:
            if role is not None:
                current_locations = self.find_practitioner_role_locations(role)

                for location in current_locations:
                    if location is not None:
                        practitioner_locations.append(location)

        return practitioners, practitioner_roles, practitioner_locations

    def flatten_data(self):
        self.Flatten.flatten_all()

    def role_unique_key(self, role):
        # Generate a unique key for the role. Adjust this based on available unique attributes.
        return f"{role.resource_type}-{role.id}"

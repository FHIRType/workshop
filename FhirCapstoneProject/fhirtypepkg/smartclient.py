# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Functionality to connect to and interact with Endpoints.
import asyncio
import http.client
import json
import ssl
import subprocess
from typing import Any

import aiohttp
import fhirclient.models.bundle
import fhirclient.models.location as loc
import fhirclient.models.organization as org
import fhirclient.models.practitioner as prac
import fhirclient.models.practitionerrole as prac_role
import requests
import requests.adapters
from fhirclient import client
from fhirclient.models.capabilitystatement import CapabilityStatement
from fhirclient.models.domainresource import DomainResource
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirsearch import FHIRSearch
from requests.exceptions import HTTPError
from requests.exceptions import SSLError

import FhirCapstoneProject.fhirtypepkg as fhirtypepkg
from FhirCapstoneProject.fhirtypepkg.curl_to_requests import (
    FakeSocket,
    FakeHTTPResponse,
)
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.fhirtype import ExceptionNPI
from FhirCapstoneProject.fhirtypepkg.fhirtype import fhir_logger
from FhirCapstoneProject.fhirtypepkg.flatten import (
    validate_npi,
)
from FhirCapstoneProject.fhirtypepkg.localization import localize


def resolve_reference(_smart, reference: fhirclient.models.fhirreference.FHIRReference):
    """
    :param _smart:
    :param reference:
    :return: JSON Object of the resolved reference (hint: __init__ DomainResource with this return)
    """
    reference = reference.reference

    if reference is None:
        raise TypeError("FHIRReference to None")

    return _smart._http_json_query(reference, [])


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
            localize("family"): name_family,
            localize("given"): name_given,
            localize("identifier"): npi,
        }
    )


def http_build_search_practitioner_role(practitioner: prac.Practitioner) -> list:
    """
    Simply extends `::fhirtypepkg.client.http_build_search` to build a list of 2-tuples specifically
    for practitioner roles
    """
    return http_build_search({localize("practitioner"): practitioner.id})


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
    parameters = {localize("family"): name_family, localize("given"): name_given}

    if npi is not None:
        try:
            parameters[localize("identifier")] = validate_npi(npi)
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
    parameters = {localize("practitioner"): practitioner.id}

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
    def __init__(self, _endpoint: Endpoint):
        """
        Initializes a SmartClient for the given Endpoint. Assumes the Endpoint is properly initialized.

        :param _endpoint: A valid Endpoint object
        :param get_metadata: Whether to perform `::fhirtypepkg.client.SmartClient.find_endpoint_metadata`
        upon instantiation, if set to false this can always be called later.
        """
        self._can_search_by_npi = _endpoint.can_search_by_npi

        self.endpoint = _endpoint

        # TODO: Fail gracefully when an endpoint is down
        self.smart = client.FHIRClient(
            settings={
                localize("app id"): fhirtypepkg.fhirtype.get_app_id(),
                localize("api base"): _endpoint.get_url(),
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
        self._http_client_list = []
        self._http_client_mutex = 0
        if self.endpoint.use_http_client:
            fhir_logger().info(
                "USE CLIENT.HTTP Connection per config for endpoint %s (%s), this will override use of the FHIR Client.",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )
            self._enable_http_client = True

        # If there has been a metadata endpoint configured for this endpoint, and it doesn't use the HTTP Client method,
        # attempt to collect its metadata.
        if (
            self.endpoint.get_metadata_on_init is not False
            and not self._enable_http_client
        ):
            self.metadata = self.find_endpoint_metadata(
                self.endpoint.get_metadata_on_init
            )
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

            prac_params = self._search_params.get(localize("npi code"), None)

            if prac_params is not None and localize("identifier") in prac_params:
                self._can_search_by_npi = True

    # def init_flatten_class(self):
    #     self.Flatten = FlattenSmartOnFHIRObject(self.get_endpoint_name())

    def _get_http_client(self) -> http.client.HTTPSConnection:
        self._http_client_mutex += 1
        connection = http.client.HTTPSConnection(self.endpoint.host)
        self._http_client_list.append(connection)

        return connection

    def _release_http_client(self):
        self._http_client_mutex -= 1
        if len(self._http_client_list) > 0 and self._http_client_mutex <= 0:
            for client in self._http_client_list:
                client.close()

            self._http_client_list = []

    def _is_http_session_confirmed(self) -> bool or None:
        """
        Returns value of protected flag, this flag is updated any time an HTTP request is made
        """
        return self._http_session_confirmed

    def _initialize_http_session(self):
        """
        Creates an HTTP session for this SmartClient and attempts to verify the connection,
        handles any failures to connect and logs using `::fhirtypepkg.logging_fhir.FHIRLogger`
        """
        self.http_session.auth = ("", "")  # TODO: Authentication stretch goals

        try:
            # Initialize HTTP connection by collecting metadata
            if self.endpoint.get_metadata_on_init is False:
                raise Exception(
                    f"MISCONFIGURED ENDPOINT [{self.get_endpoint_name()}]: An HTTP session is being "
                    f"attempted without a metadata endpoint, please configure 'get_metadata_on_init' to a "
                    f"valid path in the Endpoint configuration file."
                )

            response = self.http_session.get(
                self.endpoint.get_url() + self.endpoint.get_metadata_on_init
            )

            if 200 <= response.status_code < 400:
                self._http_session_confirmed = True
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

    def _http_query(self, query: str, params: list) -> requests.Response:
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

            # Generate an HTTP Response from a curl
            # Perform an OS level https request and store the output bytes
            try:
                output = subprocess.check_output(
                    ["curl", "-s", "-k", "-D", "-", query_url]
                )

                # Decode the output and parse it as JSON

                curl_wrapper = FakeSocket(output)
                curl_response = FakeHTTPResponse(curl_wrapper)

                request_parse = requests.PreparedRequest()
                request_parse.url = query_url

                adapter = requests.adapters.HTTPAdapter()
                response = adapter.build_response(request_parse, curl_response)

            except subprocess.CalledProcessError as e:
                response = FakeHTTPResponse(None)

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
            if self._enable_http_client:
                raise requests.RequestException(response=response)
            else:
                raise requests.RequestException(
                    response=response, request=response.request
                )

        return response

    async def _async_http_query(self, query: str, params: list) -> str:
        """
        Sends a query to the API via an asynchronous HTTP GET request and returns the body string unchanged. Cannot
        be used with HTTP_Client_Enabled

        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A string, the body of the response
        """
        # Stage the connection to this endpoint
        connector = aiohttp.TCPConnector(limit=400)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        # Build the query url
        query_url = self.endpoint.get_url() + query
        query_url += "?"
        for param in params:
            query_url += param[0]
            query_url += "="
            query_url += param[1]
            query_url += "&"
        query_url = query_url[:-1]

        async with aiohttp.ClientSession(
            connector=connector, timeout=aiohttp.ClientTimeout(6000), headers=headers
        ) as session:
            async with session.get(query_url) as response:
                if response.status != 200:
                    fhir_logger().error("Query Url: ", query_url)
                    raise aiohttp.ClientResponseError
                else:
                    return await response.text()

    def _http_json_query(self, query: str, params: list) -> dict:
        """
        Sends a query to the API via an HTTP GET request, accepts as json and deserializes.
        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A list, deserialized from json response
        """
        try:
            response = self._http_query(query, params=params)
        except requests.RequestException as e:
            return {}

        # Used to check the content type of the response, only accepts those types specified in fhirtype
        content_type = fhirtypepkg.fhirtype.parse_content_type_header(
            response.headers["content-type"]
        )

        output = json.loads(response.text)

        if self._enable_http_client:
            self._release_http_client()

        try:
            # dict (analog of Location) / dict (analog of Organization)
            # If the response has a LOCATION or ORGANIZATION reference, resolve that to a DomainResources from a dict
            for h in range(len(output)):
                domain_resource = output[h]
                if hasattr(domain_resource, localize("location")):
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

                if hasattr(domain_resource, localize("organization")):
                    if type(domain_resource.organization) is list:
                        for i in range(len(domain_resource.organization)):
                            output[h].organization[i] = org.Organization(
                                resolve_reference(self, domain_resource.organization[i])
                            )

                    elif (
                        type(domain_resource.organization)
                        is fhirclient.models.fhirreference.FHIRReference
                    ):
                        output[h].organization = org.Organization(
                            resolve_reference(self, domain_resource.organization)
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

    async def _async_http_json_query(self, query: str, params: list) -> dict:
        """
        Sends an ASYNCHRONOUS query to the API via an HTTP GET request, accepts as json and deserializes.
        :param query: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param params: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A list, deserialized from json response
        """
        try:
            response = await self._async_http_query(query, params=params)
        except requests.RequestException as e:
            return {}

        output = json.loads(response)

        return output

    def _parse_json_to_domain_resources(self, res: dict) -> list:
        """
        Sends a query to the API via an HTTP GET request, parses to a list of FHIR Resources.
        :param self: The query to perform against the endpoint's URL (e.g. endpoint.com/QUERY)
        :param res: A list of 2-tuples of parameters (e.g. [(A, 1)] would yield endpoint.com/QUERY?A=1),
        or an empty list to include no parameters
        :return: A list of FHIR Resources
        """

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
                if hasattr(domain_resource, localize("location")):
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

                if hasattr(domain_resource, localize("organization")):
                    if type(domain_resource.organization) is list:
                        for i in range(len(domain_resource.organization)):
                            parsed[h].organization[i] = org.Organization(
                                resolve_reference(self, domain_resource.organization[i])
                            )

                    elif (
                        type(domain_resource.organization)
                        is fhirclient.models.fhirreference.FHIRReference
                    ):
                        parsed[h].organization = org.Organization(
                            resolve_reference(self, domain_resource.organization)
                        )

        except TypeError as e:
            fhir_logger().warning(
                "Caught a TypeError while resolving a reference, could have been a None reference. (%s)",
                e,
            )

        return parsed

    def _fhir_query(self, search: FHIRSearch, resolve_references=True) -> list:
        """
        Returns the results of a search performed against this SmartClient's server
        :type search: FHIRSearch
        :param search: Arbitrary search, see `build_search`
        :rtype: list
        :return: Results of the search
        """
        output = None

        try:
            output = search.perform_resources(self.smart.server)
        except FHIRValidationError as e:
            fhir_logger().exception(
                f"## FHIRValidationError: {e}"
            )  # TODO: Need to understand this exception
        except HTTPError as e:
            fhir_logger().exception(f"## HTTPError: {e}")
        except SSLError as e:
            fhir_logger().exception(f"## SSLError: {e}")

        if resolve_references:
            try:
                # List of prac.Practitioner / List of pracrole.PractitionerRole
                # If the response has a LOCATION or ORGANIZATION reference, resolve that to a DomainResources
                for h in range(len(output)):
                    domain_resource = output[h]
                    if hasattr(domain_resource, localize("location")):
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

                    if hasattr(domain_resource, localize("organization")):
                        if type(domain_resource.organization) is list:
                            for i in range(len(domain_resource.organization)):
                                output[h].organization[i] = org.Organization(
                                    resolve_reference(
                                        self, domain_resource.organization[i]
                                    )
                                )

                        elif (
                            type(domain_resource.organization)
                            is fhirclient.models.fhirreference.FHIRReference
                        ):
                            output[h].organization = org.Organization(
                                resolve_reference(self, domain_resource.organization)
                            )

            except TypeError as e:
                fhir_logger().warning(
                    "Caught a TypeError while resolving a reference, could have been a None reference. (%s)",
                    e,
                )

        return output

    async def _http_query_practitioner(
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

        res = await self._async_http_json_query(
            localize("titlecase practitioner"), search
        )
        return self._parse_json_to_domain_resources(res)

    def _fhir_query_practitioner(
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
            output = self._fhir_query(
                fhir_build_search_practitioner(name_family, name_given, npi),
                resolve_references,
            )
        else:
            output = self._fhir_query(
                fhir_build_search_practitioner(name_family, name_given, None),
                resolve_references,
            )

        return output

    async def _http_query_practitioner_role(
        self, practitioner: prac.Practitioner
    ) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner via HTTP session
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        res = await self._async_http_json_query(
            localize("title case PractitionerRole"),
            http_build_search_practitioner_role(practitioner),
        )
        return self._parse_json_to_domain_resources(res)

    def _fhir_query_practitioner_role(
        self, practitioner: prac.Practitioner, resolve_references=False
    ) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner via Smart on FHIR client
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self._fhir_query(
            fhir_build_search_practitioner_role(practitioner), resolve_references
        )

    def find_endpoint_metadata(self, request_string: str) -> CapabilityStatement:
        """
        Queries the remote endpoint via HTTP session for the endpoint's metadata (or "Capability Statement")
        :return: The Capability Statement parsed into a Smart on FHIR object
        """
        capability_via_fhir = self.smart.server.request_json(path=request_string)

        return CapabilityStatement(capability_via_fhir)

    async def find_practitioner(
        self,
        name_family: str,
        name_given: str,
        npi: str or None,
        resolve_references=True,
    ) -> list[DomainResource]:
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

        # We only use HTTP, this supports async requests whereas SmartOnFhir does not
        practitioners_response = await self._http_query_practitioner(
            name_family, name_given, npi
        )

        prac_resources, filtered_prac = [], []
        unique_identifiers = set()

        if practitioners_response and len(practitioners_response) > 0:
            for practitioner in practitioners_response:
                if type(practitioner) is prac.Practitioner and practitioner.identifier:

                    for _id in practitioner.identifier:
                        if (
                            _id.system == "http://hl7.org/fhir/sid/us-npi"
                            and _id.value == npi
                        ):
                            if practitioner.id not in unique_identifiers:
                                unique_identifiers.add(practitioner.id)
                                prac_resources.append(practitioner)

        if len(prac_resources) == 0:
            return None

        return prac_resources

    async def find_practitioner_role(
        self, practitioner: prac.Practitioner, resolve_references=False
    ) -> list[Any]:
        """
        Searches for and returns a list of roles associated with the given practitioner.

        This function queries the FHIR Client unless the endpoint was configured to use the HTTP Client (which takes priority if it is enabled) for roles associated with the practitioner passed in as a parameter.
        The roles are then standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.

        Note: The roles returned will only reflect those from the same endpoint as the practitioner was selected from.

        Parameters:
            resolve_references:
        :param resolve_references: Condition to determine whether to resolve references or not
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
            practitioner_roles_response = await self._http_query_practitioner_role(
                practitioner
            )
        else:
            practitioner_roles_response = self._fhir_query_practitioner_role(
                practitioner, resolve_references
            )

        if not practitioner_roles_response:
            return None

        seen_roles = set()  # Track seen roles to avoid duplicates
        for role in practitioner_roles_response:
            if role.id not in seen_roles:
                seen_roles.add(role.id)
                prac_roles.append(role)

        if len(prac_roles) == 0:
            return None

        return prac_roles

    def find_practitioner_role_locations(
        self, practitioner_role: prac_role.PractitionerRole
    ) -> list[Any]:
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
                locations.append(role_location)

        if len(locations) == 0:
            return None

        return locations

    async def find_all_practitioner_data(
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
        :param resolve_references: Condition to determine whether to resolve references or not

        Returns:
        """

        # Find all associated practitioners from this client's remote endpoint
        practitioners = await self.find_practitioner(
            name_family, name_given, npi, resolve_references
        )

        if practitioners is None:
            return None, None, None

        # Find all associated practitioners roles from this client's remote endpoint
        practitioner_roles = []
        for practitioner in practitioners:
            practitioner_roles_response = await self.find_practitioner_role(
                practitioner, resolve_references
            )

            if practitioner_roles_response is not None:
                for role in practitioner_roles_response:
                    practitioner_roles.append(role)

        if practitioner_roles is None:
            return practitioners, None, None

        # Find all associated practitioners roles locations from this client's remote endpoint
        practitioner_locations = []
        for role in practitioner_roles:
            current_locations = self.find_practitioner_role_locations(role)
            for location in current_locations:
                practitioner_locations.append(location)

        if practitioner_locations is None:
            return practitioners, practitioner_roles, None

        return practitioners, practitioner_roles, practitioner_locations

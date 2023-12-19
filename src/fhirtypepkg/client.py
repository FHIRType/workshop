# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Functionality to connect to and interact with Endpoints. Much of the functionality borrowed from code
# provided by Kevin.
import os
import ssl
import json
from typing import Tuple, List, Any

import fhirclient.models.bundle
import requests
import re

from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
import fhirclient.models.organization as org
import fhirclient.models.fhirreference as fhirreference
from fhirclient.models.domainresource import DomainResource
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.capabilitystatement import CapabilityStatement

from requests.exceptions import SSLError
from requests.exceptions import HTTPError

import src.fhirtypepkg as fhirtypepkg
from src.fhirtypepkg.fhirtype import ExceptionNPI
from src.fhirtypepkg.endpoint import Endpoint
from src.fhirtypepkg.fhirtype import fhir_logger
from src.fhirtypepkg.standardize import StandardizedResource, validate_npi


def resolve_reference(_smart, reference: fhirclient.models.fhirreference.FHIRReference):
    """
    TODO: Doc]\s
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
        self._can_search_by_npi = False

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

        self.Standardized = (
            StandardizedResource()
        )  # The StandardizedResource object is used to transform raw FHIR data into a more accessible format.

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
            response = self.http_session.get(self.endpoint.get_url() + "metadata")

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
            fhir_logger().error(f"SSLCertVerificationError:", e)

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

        if self._http_session_confirmed is None:
            fhir_logger().error(
                "Attempted to make HTTP Query without HTTP Session enabled on %s (%s).",
                self.get_endpoint_name(),
                self.get_endpoint_url(),
            )
            raise HTTPError

        # Checks HTTP session and attempts to reestablish if unsuccessful.
        if not self._http_session_confirmed:
            self._initialize_http_session()
            raise Exception(
                "No HTTP Connection, try reestablishing."
            )  # TODO: This may be handled differently

        # Only include the params list if there are params to include, otherwise Requests gets mad
        if len(params) > 0:
            response = self.http_session.get(
                self.endpoint.get_url() + query, params=params
            )
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

                if hasattr(domain_resource, "organization"):  # TODO: localization
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

                if hasattr(domain_resource, "organization"):  # TODO: localization
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

    def fhir_query(self, search: FHIRSearch) -> list:
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
            fhir_logger().error(
                f"## FHIRValidationError: {e}"
            )  # TODO: Need to understand this exception
        except HTTPError as e:
            fhir_logger().error(
                f"## HTTPError: {e}"
            )  # TODO: Probably need to notify and maybe trigger reconnect here
        except SSLError as e:
            fhir_logger().error(
                f"## SSLError: {e}"
            )  # TODO: Probably need to notify and maybe trigger reconnect here

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

                if hasattr(domain_resource, "organization"):  # TODO: localization
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
        self, name_family: str, name_given: str, npi: str or None
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
                fhir_build_search_practitioner(name_family, name_given, npi)
            )
        else:
            output = self.fhir_query(
                fhir_build_search_practitioner(name_family, name_given, None)
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

    def fhir_query_practitioner_role(self, practitioner: prac.Practitioner) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner via Smart on FHIR client
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self.fhir_query(fhir_build_search_practitioner_role(practitioner))

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
        self, name_family: str, name_given: str, npi: str or None
    ) -> tuple[list[DomainResource], list[dict]]:
        """
        Searches for practitioners by first name, last name, and NPI (National Provider Identifier).

        This function first queries the FHIR server by first name and last name, then checks the NPI of the returned practitioners.
        If a practitioner's NPI matches the provided NPI, the function returns a list containing a single practitioner object and a dictionary of standardized practitioner data.

        The practitioner data is standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.


        Parameters:
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
        practitioners_via_fhir = self.fhir_query_practitioner(
            name_family, name_given, npi
        )
        # practitioners_via_http = self.http_query_practitioner(last_name, first_name, npi)

        prac_resources, filterd_pracs = [], []
        unique_identifiers = set()

        if practitioners_via_fhir:
            for practitioner in practitioners_via_fhir:
                if practitioner.identifier:
                    self.Standardized.setPractitioner(practitioner)
                    for _id in practitioner.identifier:
                        if (
                            (npi is not None or npi != "")
                            and _id.system == "http://hl7.org/fhir/sid/us-npi"
                            and _id.value == npi
                        ) or (npi is None or npi == ""):
                            if practitioner.id not in unique_identifiers:
                                prac_resources.append(self.Standardized.RESOURCE)
                                filterd_pracs.append(
                                    self.Standardized.PRACTITIONER.filtered_dictionary
                                )
                                unique_identifiers.add(practitioner.id)

        return prac_resources, filterd_pracs

    # def find_practitioner_role(self, practitioner: prac.Practitioner) -> list:
    def find_practitioner_role(
        self, practitioner: prac.Practitioner
    ) -> tuple[list[Any], dict]:
        """
        Searches for and returns a list of roles associated with the given practitioner.

        This function queries the FHIR server for roles associated with the practitioner passed in as a parameter.
        The roles are then standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.

        Note: The roles returned will only reflect those from the same endpoint as the practitioner was selected from.

        Parameters:
        :param practitioner: A Practitioner object for which to find associated roles.
        :type practitioner: fhirclient.models.practitioner.Practitioner

        Returns:
        :rtype: tuple(list, dict)
        :return tuple: A tuple containing two elements:
            - list: A list of practitioner roles (as FHIR resources) associated with the given practitioner.
            - dict: A dictionary of standardized data for the practitioner roles. If no roles are found, an empty dictionary is returned.
        """
        prac_roles, filtered_roles = [], []
        practitioner_roles_via_fhir = self.fhir_query_practitioner_role(practitioner)

        if not practitioner_roles_via_fhir:
            return [], {}

        for role in practitioner_roles_via_fhir:
            self.Standardized.setPractitionerRole(role)
            prac_roles.append(self.Standardized.RESOURCE)
            filtered_roles.append(
                self.Standardized.PRACTITIONER_ROLE.filtered_dictionary
            )

        return prac_roles, filtered_roles

    def find_practitioner_role_locations(
        self, practitioner_role: prac_role.PractitionerRole
    ) -> tuple[list[Any], dict]:
        """
        Searches for and returns a list of locations associated with a given practitioner role.

        This function queries the FHIR server for locations associated with the practitioner role passed in as a parameter.
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

        for role_location in practitioner_role.location:
            # # If the response is already a Location resource, return that
            # if type(role_location) is loc.Location:
            #     role_location = role_location.Location.read_from(
            #         role_location.reference, self.smart.server
            #     )
            #
            # # If the response is a reference, resolve that to a Location and return that
            # if type(role_location) is fhirclient.models.fhirreference.FHIRReference:
            #     reference = role_location.reference
            #
            #     res = self.http_json_query(reference, [])
            #
            #     role_location = loc.Location(res)

            # Standardize the locations
            self.Standardized.setLocation(role_location)
            locations.append(self.Standardized.RESOURCE)
            filtered_dictionary.append(self.Standardized.LOCATION.filtered_dictionary)

        return locations, filtered_dictionary

    # def find_practitioner_role_organization(self, practitioner_role: prac_role.PractitionerRole) -> list:
    def find_practitioner_role_organization(
        self, practitioner_role: prac_role.PractitionerRole
    ) -> tuple[list[Any], dict]:
        """
        Searches for and returns an organization associated with a given practitioner role.

        This function queries the FHIR server for the organization associated with the practitioner role passed in as a parameter.
        Each organization could represent a place where the practitioner works. For example, if Dr Alice Smith works at the organization Top Medical Group using her cardiology role, the organization would be returned.

        The organization is then standardized using the `Standardized` object of the `SmartClient` class, which transforms the raw FHIR data into a more accessible format.

        Parameters:
        :param practitioner_role: A PractitionerRole object for which to find associated organization.
        :type practitioner_role: fhirclient.models.practitionerrole.PractitionerRole

        Returns:
        :rtype: tuple(list, dict)
        :return tuple: A tuple containing two elements:
            - list: A list of organizations (as FHIR resources) associated with the given practitioner role. If no organization is found, a list containing None is returned.
            - dict: A dictionary of standardized data for the organization. If no organization is found, an empty dictionary is returned.
        """
        organizations, filtered_dictionary = [], []

        # None references get through to here sometimes, if they do they will have a None id
        if practitioner_role.organization is not None and practitioner_role.organization.id is not None:
            # print("Organization: ", practitioner_role.organization.as_json())
            # print("Reference: ", practitioner_role.organization.reference)
            # organization = org.Organization.read_from(  # TODO: Use this, dumbass.
            #     practitioner_role.organization.reference, self.smart.server
            # )

            # Standardize the organizations
            self.Standardized.setOrganization(practitioner_role.organization)
            organizations.append(self.Standardized.RESOURCE)
            filtered_dictionary.append(
                self.Standardized.ORGANIZATION.filtered_dictionary
            )

        return organizations, filtered_dictionary

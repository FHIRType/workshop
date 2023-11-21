# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Functionality to connect to and interact with Endpoints. Much of the functionality borrowed from code
# provided by Kevin.
import os
import ssl
import json

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

from requests.exceptions import SSLError
from requests.exceptions import HTTPError

import fhirtypepkg
from fhirtypepkg.fhirtype import ExceptionNPI
from fhirtypepkg.endpoint import Endpoint
from fhirtypepkg.fhirtype import fhir_logger


def validate_npi(npi: str) -> str:
    """
    Validates that a given string may be an NPI; this is a simple format test and does NOT check against any databases
        Will raise ExceptionNPI if invalid, always returns a valid NPI.
    :return: A valid NPI of the form "0000000000"
    """
    m = re.match(r'([0-9]{10})', npi)

    if m is None:
        raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")
    else:
        valid_npi = m.group(0)

    if valid_npi is None:
        raise ExceptionNPI(f"Invalid NPI (expected form:  000000000): {npi}")

    return m.group(0)


def http_build_search(parameters: dict) -> list:
    output = []

    for key in parameters:
        output.append((key, parameters[key]))

    return output


def http_build_search_practitioner(name_family: str, name_given: str, npi: str) -> list:
    return http_build_search({"family": name_family, "given": name_given, "identifier": npi})  # TODO maybe its identifier


def http_build_search_practitioner_role(practitioner: prac.Practitioner) -> list:
    return http_build_search({"practitioner": practitioner.id})


def fhir_build_search(resource: DomainResource, parameters: dict) -> FHIRSearch:
    """
    Builds an arbitrary search object for the given DomainResource
    (e.g. `fhirclient.models.practitioner.Practitioner` or `fhirclient.models.location.Location`)
    using the given parameters.
        Does not validate parameters against the resource's model.
    :param resource: DomainResource (e.g. `fhirclient.models.practitioner.Practitioner`)
    :param parameters: A dict of valid parameters for that resource.
    :return: A search which can be performed against a client's server.
    """
    return resource.where(struct=parameters)


def fhir_build_search_practitioner(name_family: str, name_given: str, npi: str) -> FHIRSearch:
    """
    Builds a search object for the DomainResource `Practitioner` from a name and NPI.
    Will perform a validation on the NPI.
        TODO: NPI is suppressed while research into different endpoint's model
         validation is done.  (See FHIRValidationError)
    :param name_given: Given name, or first name, of the search
    :param name_family: Family name, or last name, of the search
    :param npi: [formatted 0000000000] National Physician Identifier
    :return: A search which can be performed against a client's server.
    """
    try:
        npi = validate_npi(npi)
    except ExceptionNPI:
        npi = None

    parameters = {
        "family": name_family,
        "given": name_given,
        # "npi": npi  # TODO: Suppressing this until we better understand each endpoints' model validation
    }

    return fhir_build_search(prac.Practitioner, parameters)


def fhir_build_search_practitioner_role(practitioner: prac.Practitioner) -> FHIRSearch:
    """
    Builds a search object for the DomainResource `PractitionerRole` from a valid `Practitioner` DomainResource,
    this search is intended to find the `PractitionerRoles` associated with that valid `Practitioner`.
    :param practitioner: A valid DomainResource `Practitioner`
    :return: A search which can be performed against a client's server.
    """
    parameters = {
        "practitioner": practitioner.id
    }

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

    http_session_confirmed
        Whenever an HTTP request is made, the status is checked and updated here
    """

    http_session_confirmed: bool

    def __init__(self, endpoint: Endpoint):
        """
        Initializes a SmartClient for the given Endpoint. Assumes the Endpoint is properly initialized.

        :param endpoint: A valid Endpoint object
        """
        self.endpoint = endpoint

        self.smart = client.FHIRClient(settings={'app_id': fhirtypepkg.fhirtype.get_app_id(),
                                                 'api_base': endpoint.get_endpoint_url()})

        self.http_session = requests.Session()
        self.http_session_confirmed = False
        self._initialize_http_session()

    def _initialize_http_session(self):
        # self.http_session.auth = (None, None)  # TODO: Authentication as needed
        self.http_session.auth = ("", "")

        # TODO [Logging]: This whole block is a consideration for Logging
        try:
            # Initialize HTTP connection by collecting metadata
            p = [("Accept", "application/json")]
            response = self.http_session.get(self.endpoint.get_endpoint_url() + "metadata", params=p)

            if 200 <= response.status_code < 300:
                # TODO: Do capability parsing @trentonyo
                self.http_session_confirmed = True
            else:
                raise requests.RequestException(response=response, request=response.request)
                # TODO Actually response codes, and the above should be a finally after the usual suspects
        except requests.RequestException as e:
            print(f"Error making HTTP request: {e}")
            # TODO: Handle exceptions appropriately
        except ssl.SSLCertVerificationError as e:
            print(f"SSLCertVerificationError: {e}")

        if self.http_session_confirmed:
            fhir_logger().info("HTTP connection established to endpoint %s (%s).", self.get_endpoint_name(), self.get_endpoint_url())
        else:
            fhir_logger().error("HTTP connection to %s (%s) failed. Try again later.", self.get_endpoint_name(), self.get_endpoint_url())

    def get_endpoint_url(self):
        return self.endpoint.get_endpoint_url()

    def get_endpoint_name(self):
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

        # Checks HTTP session and attempts to reestablish if unsuccessful.
        if not self.http_session_confirmed:
            self._initialize_http_session()
            raise Exception("No HTTP Connection, reestablishing.")  # TODO: This may be handled differently

        # Only include the params list if there are params to include, otherwise Requests gets mad
        if len(params) > 0:
            response = self.http_session.get(self.endpoint.get_endpoint_url() + query, params=params)
        else:
            response = self.http_session.get(self.endpoint.get_endpoint_url() + query)

        # Check the status
        if 200 <= response.status_code < 300:
            self.http_session_confirmed = True
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
        # response = self.http_query(self.endpoint.get_endpoint_url() + query, params=params)
        response = self.http_query(query, params=params)

        # Used to check the content type of the response, only accepts those types specified in fhirtype
        content_type = fhirtypepkg.fhirtype.parse_content_type_header(response.headers["content-type"])

        if fhirtypepkg.fhirtype.content_type_is_json(content_type):
            return json.loads(response.text)
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

        # Initialize a bundle from the response
        bundle = fhirclient.models.bundle.Bundle(res)

        # Parse each entry in the bundle to the appropriate FHIR Resource, this bundle may contain different Resources
        parsed = []
        if bundle and bundle.entry:
            for entry in bundle.entry:
                if entry:
                    parsed.append(entry.resource)

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
        except FHIRValidationError:
            print(f"## FHIRValidationError: ")  # TODO: Need to understand this exception
        except HTTPError:
            print(f"## HTTPError: ")  # TODO: Probably need to notify and maybe trigger reconnect here
        except SSLError:
            print(f"## SSLError: ")  # TODO: Probably need to notify and maybe trigger reconnect here

        return output

    def http_query_practitioner(self, name_family: str, name_given: str, npi: str) -> list:
        return self.http_fhirjson_query("Practitioner", http_build_search_practitioner(name_family, name_given, npi))

    def fhir_query_practitioner(self, name_family: str, name_given: str, npi: str) -> list:
        """
        Generates a search with the given parameters and performs it against this SmartClient's server
            Note: Searching by NPI may take additional time as not all endpoints include it as a primary key.
        :param name_given: Given name, or first name, of the search
        :param name_family: Family name, or last name, of the search
        :param npi: [formatted 0000000000] National Physician Identifier
        :rtype: list
        :return: Results of the search
        """
        return self.fhir_query(fhir_build_search_practitioner(name_family, name_given, npi))


    def http_query_practitioner_role(self, practitioner: prac.Practitioner) -> list:
        return self.http_fhirjson_query("PractitionerRole", http_build_search_practitioner_role(practitioner))


    def fhir_query_practitioner_role(self, practitioner: prac.Practitioner) -> list:
        """
        Searches for the PractitionerRole of the supplied Practitioner
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self.fhir_query(fhir_build_search_practitioner_role(practitioner))


    def find_practitioner(self, first_name: str, last_name: str, npi: str) -> list:
        """
        TODO: Need to refactor to use "given_name" and "family_name"
        This is the doctor as a person and not as a role, like Dr Alice Smith's name, NPI, licenses, specialty, etc
        This function finds a list of practitioners by first name, last name, and NPI
        It will first query by first name and last name, then check the NPI

        If it matches NPI it will return a list containing a single practitioner object,
        TODO: This is a stand-in for the consensus model
        """
        practitioners_via_fhir = self.fhir_query_practitioner(last_name, first_name, npi)
        # practitioners_via_http = self.http_query_practitioner(last_name, first_name, npi)

        # Parse results for correct practitioner
        if practitioners_via_fhir:  # If the search yielded results...
            for practitioner in practitioners_via_fhir:  # Iterate through those results.

                # TODO: standardize(practitioner)

                if practitioner.identifier:  # If the practitioner has (an) identifier(s)...
                    for _id in practitioner.identifier:  # Iterate through those identifiers,
                        # Check if the identifier is an NPI and the NPI matches the search
                        if len(npi) > 0 and _id.system == "http://hl7.org/fhir/sid/us-npi" and _id.value == npi:
                            return [practitioner]  # TODO: This is a stand in for the consensus model

        return practitioners_via_fhir

    def find_practitioner_role(self, practitioner: prac.Practitioner) -> list:
        """
        This function finds a list of roles associated with the practitioner passed in.
        TODO: This will only reflect those roles from the same endpoint as this practitioner was selected from.
        """
        practitioner_roles_via_fhir = self.fhir_query_practitioner_role(practitioner)
        # practitioner_roles_via_http = self.http_query_practitioner_role(practitioner)

        # Standardize results
        for practitioner_role in practitioner_roles_via_fhir:
            pass
            # TODO: standardize(practitioner_role)

        return practitioner_roles_via_fhir

    def find_practitioner_role_locations(self, practitioner_role: prac_role.PractitionerRole) -> list:
        """
        This function finds a location associated with a practitioner role
        So this would be a location where a doctor works, it could return multiple locations for a single role
        So Dr Alice Smith works at the hospital on 123 Main St using her cardiology role
        and Dr Alice Smith works at the clinic on 456 Main St using her neurology role
        """
        locations = []

        for role_location in practitioner_role.location:

            # If the response is already a Location resource, return that
            if type(role_location) is loc.Location:
                role_location = role_location.Location.read_from(role_location.reference, self.smart.server)

            # If the response is a reference, resolve that to a Location and return that
            if type(role_location) is fhirclient.models.fhirreference.FHIRReference:
                reference = role_location.reference

                res = self.http_json_query(reference, [])

                role_location = loc.Location(res)

            # TODO: Implement HTTP method

            # TODO: standardize(location)

            locations.append(role_location)

        return locations

    def find_practitioner_role_organization(self, practitioner_role: prac_role.PractitionerRole) -> list:
        """
        This function finds an organization associated with a practitioner role
        So this would be an organization where a doctor works, it could return multiple organizations for a single role
        So Dr Alice Smith works at the  organization Top Medical Group on 123 Main St using her cardiology role
        """
        if practitioner_role.organization:
            organization = org.Organization.read_from(practitioner_role.organization.reference, self.smart.server)

            # TODO: Implement HTTP method

            # TODO: standardize(organization)
        
            return [organization]
        else:
            return [None]


# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Functionality to connect to and interact with Endpoints. Much of the functionality borrowed from code
# provided by Kevin.
import re

from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
import fhirclient.models.organization as org
from fhirclient.models.domainresource import DomainResource
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirsearch import FHIRSearch

from requests.exceptions import SSLError
from requests.exceptions import HTTPError

import fhirtype
from fhirtype import ExceptionNPI
from endpoint import Endpoint


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


def build_search(resource: DomainResource, parameters: dict) -> FHIRSearch:
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


def build_search_practitioner(name_family: str, name_given: str, npi: str) -> FHIRSearch:
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

    return build_search(prac.Practitioner, parameters)


def build_search_practitioner_role(practitioner: prac.Practitioner) -> FHIRSearch:
    """
    Builds a search object for the DomainResource `PractitionerRole` from a valid `Practitioner` DomainResource,
    this search is intended to find the `PractitionerRoles` associated with that valid `Practitioner`.
    :param practitioner: A valid DomainResource `Practitioner`
    :return: A search which can be performed against a client's server.
    """
    parameters = {
        "practitioner": practitioner.id  # TODO (Notes from last implementation, Iain): Incomplete
                                         #  Searches recourse type, pulls bundle. Can
                                         #  deseralize into an object that has the data
                                         #  already instantialized
                                         #  Use some premade models first to mess around
    }

    return build_search(prac_role.PractitionerRole, parameters)


class SmartClient:
    """
    Initialize a class object to the provided endpoint. Should allow us to be connected to multiple endpoints
    at once with different class objects
    """
    def __init__(self, endpoint: Endpoint):
        self.smart = client.FHIRClient(settings={'app_id': fhirtype.get_app_id(),
                                                 'api_base': endpoint.get_endpoint_url()})

    def query(self, search: FHIRSearch) -> list:
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
        except FHIRValidationError:
            print(f"## FHIRValidationError: ")  # TODO: Need to understand this exception
        except HTTPError:
            print(f"## HTTPError: ")  # TODO: Probably need to notify and maybe trigger reconnect here
        except SSLError:
            print(f"## SSLError: ")  # TODO: Probably need to notify and maybe trigger reconnect here

        return output

    def query_practitioner(self, name_family: str, name_given: str, npi: str) -> list:
        """
        Generates a search with the given parameters and performs it against this SmartClient's server
            Note: Searching by NPI may take additional time as not all endpoints include it as a primary key.
        :param name_given: Given name, or first name, of the search
        :param name_family: Family name, or last name, of the search
        :param npi: [formatted 0000000000] National Physician Identifier
        :rtype: list
        :return: Results of the search
        """
        return self.query(build_search_practitioner(name_family, name_given, npi))

    def query_practitioner_role(self, practitioner: prac.Practitioner) -> list:  # TODO: Does this return a list or
                                                                                 #  is it one PractitionerRole?
        """
        Searches for the PractitionerRole of the supplied Practitioner
        :type practitioner: fhirclient.models.practitioner.Practitioner
        :param practitioner: A Practitioner object
        :rtype: list
        :return: Results of the search
        """
        return self.query(build_search_practitioner_role(practitioner))

    def find_provider(self, first_name: str, last_name: str, npi: str) -> object:
        """
        This function finds a practitioner by first name, last name, and NPI
        It will first query by first name and last name, then check the NPI
        If it matches NPI it will return a practitioner object
        This is the doctor as a person and not as a role, like Dr Alice Smith's name, NPI, licenses, specialty, etc
        """

        practitioners = self.query_practitioner(last_name, first_name, npi)  # Uses the query building methods now

        # Parse results for correct practitioner

        if practitioners:  # If the search yielded results...
            for practitioner in practitioners:  # Iterate through those results.
                if practitioner.identifier:  # If the practitioner has (an) identifier(s)...
                    # TODO: Probably need to do some more validation here, is it possible for a practitioner
                    #  to have no identifiers?
                    for _id in practitioner.identifier:  # Iterate through those identifiers,
                        # Check if the identifier is an NPI and the NPI matches the search
                        if _id.system == "http://hl7.org/fhir/sid/us-npi" and _id.value == npi:
                            return practitioner
        return None

    def find_practitioner_role(self, practitioner: prac.Practitioner) -> object:
        practitioner_roles = self.query_practitioner_role(practitioner.id)  # Uses the query building methods now

        print("num roles: ", len(practitioner_roles))

        # print results
        for practitioner_role in practitioner_roles:
            print(practitioner_role.as_json())
        return practitioner_roles
    
    def find_prac_role_locations(self, prac_role:object) -> object:
        """
        This function finds a location associated with a practitioner role
        So this would be a location where a doctor works, it could return multiple locations for a single role
        So Dr Alice Smith works at the hospital on 123 Main St using her cardiology role
        and Dr Alice Smith works at the clinic on 456 Main St using her neurology role
        """
        locations = []
        num_locations = 0
        for i in prac_role.location:
            # read the location from the reference
            location = loc.Location.read_from(i.reference, self.smart.server)
            locations.append(location)
            num_locations += 1

        print("num locations: ", len(locations))
        
        return locations
    
    def find_prac_role_organization(self, prac_role: object) -> object:

        """
        This function finds an organization associated with a practitioner role
        So this would be an organization where a doctor works, it could return multiple organizations for a single role
        So Dr Alice Smith works at the  organization Top Medical Group on 123 Main St using her cardiology role
        """

        if prac_role.organization:
            organization = org.Organization.read_from( prac_role.organization.reference, self.smart.server)
        
            return organization
        else:
            return None


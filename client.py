# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Functionality to connect to and interact with Endpoints. Much of the functionality borrowed from code
# provided by Kevin.

from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
import fhirclient.models.organization as org
from fhirclient.models.domainresource import DomainResource
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.fhirsearch import FHIRSearch
from requests.exceptions import SSLError

import fhirtype
from endpoint import Endpoint


def build_search(resource: DomainResource, parameters: dict):
    return resource.where(parameters)


def build_search_practitioner(self, name_family="", name_given="", npi="0000000000"):
    parameters = {
        "family": name_family,
        "given": name_given
    }

    return build_search(prac.Practitioner, parameters)


class SmartClient:
    """
    Initialize a class object to the provided endpoint. Should allow us to be connected to multiple endpoints
    at once with different class objects
    """
    def __init__(self, endpoint: Endpoint):
        self.smart = client.FHIRClient(settings={'app_id': fhirtype.get_app_id(),
                                                 'api_base': endpoint.get_endpoint_url()})



    def query(self, search: FHIRSearch) -> list:  # TODO: Should validate the object passed in is a valid dict for search params, unless it's always done upstream
        """
        Returns the results of a search against this SmartClient's server
        :type search: FHIRSearch
        :rtype: list
        """
        output = []

        try:
            output = search.perform_resources(self.smart.server)
        except FHIRValidationError:
            output = None  # TODO: Need to understand this exception
        except SSLError:
            output = None  # TODO: Probably need to notify and maybe trigger reconnect here

        return output

    def find_practitioner_role(self, practitioner: object) -> object:
        # build search
        search_params = {
            "practitioner": practitioner.id  # TODO incomplete
        }
        
        search = prac_role.PractitionerRole.where(struct=search_params)  # Searches recourse type, pulls bundle. Can
                                                                         # deseralize into an object that has the data
                                                                         # already instantialized
        practitioner_roles = search.perform_resources(self.smart.server)  # Use some premade models first to mess around
        print("num roles: ", len(practitioner_roles))

        # print results
        for practitioner_role in practitioner_roles:
            print(practitioner_role.as_json())
        return practitioner_roles     

    def find_provider(self, first_name: str, last_name: str, npi: str) -> object:
        """
        This function finds a practitioner by first name, last name, and NPI
        It will first query by first name and last name, then check the NPI
        If it matches NPI it will retun a practitioner object
        This is the doctor as a person and not as a role, like Dr Alice Smith's name, NPI, licenses, specialty, etc
        """
        search_params = {
            "family": last_name
            #,"given": first_name
        }

        # build search
        search = prac.Practitioner.where(struct=search_params)
        practitioners = self.query(search)

        if practitioners:
            # Parse results for correct practitioner
            for practitioner in practitioners:
                #print(practitioner.as_json())
                if practitioner.identifier:  # TODO: Need to do some more validation here, why would the identifier be null?
                    for _id in practitioner.identifier:

                        # Check if NPI matches
                        if _id.system == "http://hl7.org/fhir/sid/us-npi" and _id.value == npi:

                            return practitioner
        return None
    
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


# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Much of the functionality borrowed from code provided by Kevin

import requests
import json
import pandas as pd
from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
import fhirclient.models.organization as org
import json

# Dictionary of endpoints for each payer (Insurance Company)
endpoint_dict = {
                "kaiser_endpoint":"https://kpx-service-bus.kp.org/service/hp/mhpo/healthplanproviderv1rc",
                 "centene_endpoint":"http://production.api.centene.com/fhir/providerdirectory",
                 "cigna_endpoint":"https://p-hi2.digitaledge.cigna.com/ProviderDirectory/v1",
                 "humana_endpoint":"https://fhir.humana.com/api",
                 "pacificsource_endpoint":"https://api.apim.pacificsource.com/fhir/provider/R4"
                 }

"""
A class that gives us functionality to connect to and interact with Endpoints
"""
class smartClient:
    """
    Initialize a class object to the provided endpoint. Should allow us to be connected to multiple endpoints
    at once with different class objects
    """
    def __init__(self, endpoint: str):
        self.smart = client.FHIRClient(settings={'app_id': 'test',
                                                 'api_base': endpoint})
        
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
        practitioners = search.perform_resources(self.smart.server)

        # Parse results for correct practitioner
        for practitioner in practitioners:
            #print(practitioner.as_json())
            for id in practitioner.identifier:

                # Check if NPI matches
                if id.system == "http://hl7.org/fhir/sid/us-npi" and id.value == npi:

                    return practitioner
        return None   
    
    def find_prac_role_locations(self, prac_role:object) -> object:
        """
        This function finds a location associated with a practitioner role
        So this would be a location where a doctor works, it could return mulitple locations for a single role
        So Dr Alice Smith works at the hospital on 123 Main St using her cardiology role
        and Dr Alice Smith works at the clinic on 456 Main St using her neurology role
        """
        locations = []
        num_locations = 0
        for i in prac_role.location:
            # read the location from the reference
            location = loc.Location.read_from( i.reference, self.smart.server)
            locations.append(location)
            num_locations += 1

        print("num locations: ", len(locations))
        
        return locations
    
    def find_prac_role_organization(self, prac_role:object) -> object:

        """
        This function finds an organization associated with a practitioner role
        So this would be an organization where a doctor works, it could return mulitple organizations for a single role
        So Dr Alice Smith works at the the organization Top Medical Group on 123 Main St using her cardiology role
        """

        if prac_role.organization:
            organization = org.Organization.read_from( prac_role.organization.reference, self.smart.server)
        
            return organization
        else:
            return None
        

def print_info(info):
    """
    This function converts our info into a json, then prints it. seems a lot of the class functions return data that is in JSON format but needs to be converted first
    """

    print(json.dumps(info.as_json(), sort_keys=False, indent=2))


def main():
    humana = smartClient(endpoint_dict["humana_endpoint"])
    centene = smartClient(endpoint_dict["centene_endpoint"])
    cigna = smartClient(endpoint_dict["cigna_endpoint"])
    pacificsource = smartClient(endpoint_dict["pacificsource_endpoint"])


if __name__ == "__main__":
    main()


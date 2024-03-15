import unittest
from FhirCapstoneProject.fhirtypepkg.smartclient import SmartClient
from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from fhirclient.models.practitioner import Practitioner
from fhirclient.models.practitionerrole import PractitionerRole
from fhirclient.models.location import Location


class TestPSEndpoint(unittest.TestCase):
    """
    This is a series of integrations tests for PacificSource
    FHIR endpoints
    """

    def setUp(self):
        self.ps_endpoint = Endpoint(
            name="PacificSource",
            host="api.apim.pacificsource.com",
            address="/fhir/provider/R4/",
            secure_connection_needed=True,
            use_http_client=True,
            enable_http=False,
            get_metadata_on_init=False,
        )

        self.ps_client = SmartClient(_endpoint=self.ps_endpoint)
        self.ps_client._can_search_by_npi = True

    def test_ps_endpoint_init(self):
        """
        Just test that everythin sets up properly
        :return:
        """
        assert isinstance(self.ps_endpoint, Endpoint)
        assert isinstance(self.ps_client, SmartClient)

    def test_integration_ps_client(self):
        """
        Tests that queries return relevant FHIR resource
        :return:
        """
        # Arrange
        given_name = "Adriana"
        family_name = "Linares"
        npi = "1558577130"
        resolve_references = True

        practitioners, filtered_data = self.ps_client.find_practitioner(
            family_name, given_name, npi, resolve_references
        )

        assert isinstance(practitioners[0], Practitioner)

        prac_roles = self.ps_client.find_practitioner_role(
            practitioners[0], resolve_references
        )

        assert isinstance(prac_roles[0][0], PractitionerRole)

        location, filtered_dict = self.ps_client.find_practitioner_role_locations(
            prac_roles[0][0]
        )

        assert isinstance(location[0], Location)

    def test_integration_ps_client_with_flatten(self):
        # TODO: write tests for integration with flatten class
        assert 1 == 1

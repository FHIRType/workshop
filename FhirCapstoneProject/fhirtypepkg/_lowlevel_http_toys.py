import json
import http.client
import subprocess
import fhirclient.models.fhirreference as fhirreference

from FhirCapstoneProject.fhirtypepkg.endpoint import Endpoint
from FhirCapstoneProject.fhirtypepkg.client import SmartClient, resolve_reference


def setUp():
    output = {
        'ps_endpoint': None,
        'ps_client': None,
    }
    output['ps_endpoint'] = Endpoint(
        name="PacificSource",
        host="api.apim.pacificsource.com",
        address="/fhir/provider/R4/",
        secure_connection_needed=True,
        use_http_client=True,
        enable_http=False,
        get_metadata_on_init=False,
    )

    output['ps_client'] = SmartClient(endpoint=output['ps_endpoint'])
    output['ps_client']._can_search_by_npi = True

    return output


def ps_fhir_query(query_params: str = "Practitioner") -> dict:
    # Connect to the server using HTTP/1.1 and empty headers.
    # Unclear why it has to be this way, but on we go.

    connection = http.client.HTTPSConnection('api.apim.pacificsource.com', port=443)
    connection.request('GET', f'/fhir/provider/R4/{query_params}', headers={})
    response = connection.getresponse()
    # return response

    if response.getcode() == 200:
        # Read the response data as bytes
        response_data_bytes = response.read()

        # Decode the bytes to a string
        response_data_string = response_data_bytes.decode('utf-8')

        # Parse the string as JSON to get a dictionary
        response_data_dict = json.loads(response_data_string) #TODO I'm the other thing

        # Close the connection
        connection.close()

        return response_data_dict
    else:
        return {"error": f"Code: {response.getcode()} Message: {response.reason}"}

def subprocess_http_request(query_params: str = "Practitioner",
                            fhir_base_url: str = "https://api.apim.pacificsource.com/fhir/provider/R4/") -> dict or fhirreference.FHIRReference:

    """
    Connect to the server using OS curl
    This is admittedly not an ideal way to do this, but the host machine
    is not configured properly and does not work well with Python HTTPS libraries.
    :param query_params: The query parameter for the FHIR query
    :return: dictionary of the response json
    """
    try:
        # Use a smart client to resolve references
        ps = setUp()

        # Perform an OS level https request and store the output bytes
        output = subprocess.check_output(['curl', '-s', f"{fhir_base_url}{query_params}"])
        # Decode the output and parse it as JSON
        response_data = json.loads(output.decode('utf-8')) #TODO this looks just like the other thing
        return response_data



        # if response_data['resourceType'] == "Bundle":
        #     ref = {
        #         "resourceType": response_data['resourceType'],
        #         "id": response_data['id'],
        #         "type": response_data['type'],
        #     }
        #
        #     ref = fhirreference.FHIRReference(ref)
        #     return resolve_reference(ps['ps_client'], ref)

        return response_data

    except subprocess.CalledProcessError as e:
        return {"Error": f"Error: HTTP status code {e}"}


if __name__ == "__main__":
    thing = ps_fhir_query()
    res = subprocess_http_request(query_params="Practitioner?family=Linares&given=Adriana&identifier=1558577130")
    print(res)

# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Much of the functionality borrowed from code provided by Kevin.

import json

from endpoint import Endpoint
from client import SmartClient


endpoint_humana = Endpoint("Humana", "fhir.humana.com", "/sandbox/api/")  # Or "/api/"
endpoint_kaiser = Endpoint("Kaiser", "kpx-service-bus.kp.org", "/service/hp/mhpo/healthplanproviderv1rc/")
endpoint_cigna = Endpoint("Cigna", "p-hi2.digitaledge.cigna.com", "/ProviderDirectory/v1/")
endpoint_centene = Endpoint("Centene", "production.api.centene.com", "/fhir/providerdirectory/")
endpoint_pacificsource = Endpoint("Pacific Source", "api.apim.pacificsource.com", "/fhir/provider/R4/")

def printInfo(info):
    """
    This function converts our info into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    print(json.dumps(info.as_json(), sort_keys=False, indent=2))

def main():
    smartclient_humana = SmartClient(endpoint_humana)
    smartclient_centene = SmartClient(endpoint_centene)
    smartclient_cigna = SmartClient(endpoint_cigna)
    smartclient_kaiser = SmartClient(endpoint_kaiser)
    smartclient_pacificsource = SmartClient(endpoint_pacificsource)


if __name__ == "__main__":
    main()


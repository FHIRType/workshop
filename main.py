# Authors: Iain Richey, Trenton Young, Kevin Carman
# Description: Much of the functionality borrowed from code provided by Kevin.

import requests
import pandas as pd
import json

from fhirclient import client
import fhirclient.models.practitioner as prac
import fhirclient.models.location as loc
import fhirclient.models.practitionerrole as prac_role
import fhirclient.models.organization as org

from endpoint import Endpoint
from clientClass import SmartClient

def main():
    humana = SmartClient(endpoint_dict["humana_endpoint"])
    centene = SmartClient(endpoint_dict["centene_endpoint"])
    cigna = SmartClient(endpoint_dict["cigna_endpoint"])
    pacificsource = SmartClient(endpoint_dict["pacificsource_endpoint"])


if __name__ == "__main__":
    main()


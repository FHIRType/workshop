# Authors: Iain Richey, Trenton Young
# Description: Creates the config files needed by our program

import os
import configparser
import sys

#List of API endpoints
endpoints = [
    {'name': 'Humana', 'host': 'fhir.humana.com', 'address': '/sandbox/api/', 'ssl': 'True'},
    {'name': 'Kaiser', 'host': 'kpx-service-bus.kp.org', 'address': '/service/hp/mhpo/healthplanproviderv1rc/', 'ssl': 'True'},
    {'name': 'Cigna', 'host': 'p-hi2.digitaledge.cigna.com', 'address': '/ProviderDirectory/v1/', 'ssl': 'True'},
    {'name': 'Centene', 'host': 'production.api.centene.com', 'address': '/fhir/providerdirectory/', 'ssl': 'False'},
    # {'name': 'Pacificsource', 'host': 'api.apim.pacificsource.com', 'address': '/fhir/provider/R4/', 'ssl': 'True'}
]


def main():
    args = sys.argv[1:]

    target = f'src/fhirtypepkg/config/{args[0]}.ini'

    newconfig = configparser.ConfigParser() #create a configParser object

    for endpoint in endpoints: #loop through our endpoints
        newconfig.add_section(endpoint.get("name")) #add a section for that endpoint
        newconfig.set(endpoint.get("name"), "name", endpoint.get("name")) #add it's corresponding data
        newconfig.set(endpoint.get("name"), "host", endpoint.get("host"))
        newconfig.set(endpoint.get("name"), "address", endpoint.get("address"))
        newconfig.set(endpoint.get("name"), "ssl", endpoint.get("ssl"))

    print(f"CWD: {os.getcwd()}", f"Target: {target}", sep='\n')

    with open(target, 'w+') as configfile:
        newconfig.write(configfile)


if __name__ == "__main__":
    main()

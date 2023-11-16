# Authors: Iain Richey, Trenton Young
# Description: Creates the config files needed by our program

import os
import configparser

#Create a ConfigParser object
config = configparser.ConfigParser()

#Add a section for API endpoints
config.add_section('APIEndpoints')

#List of API endpoints
endpoints = [
    {'name': 'Humana', 'host': 'fhir.humana.com', 'address': '/sandbox/api/', 'ssl': 'True'},
        {'name': 'Kaiser', 'host': 'kpx-service-bus.kp.org', 'address': '/service/hp/mhpo/healthplanproviderv1rc/', 'ssl': 'True'},
        {'name': 'Cigna', 'host': 'p-hi2.digitaledge.cigna.com', 'address': '/ProviderDirectory/v1/', 'ssl': 'True'},
        {'name': 'Centene', 'host': 'production.api.centene.com', 'address': '/fhir/providerdirectory/', 'ssl': 'False'},
        # {'name': 'Pacificsource', 'host': 'api.apim.pacificsource.com', 'address': '/fhir/provider/R4/', 'ssl': 'True'}
]

# endpoint_humana = Endpoint("Humana", "fhir.humana.com", "/sandbox/api/")  # Or "/api/"
# endpoint_kaiser = Endpoint("Kaiser", "kpx-service-bus.kp.org", "/service/hp/mhpo/healthplanproviderv1rc/")
# endpoint_cigna = Endpoint("Cigna", "p-hi2.digitaledge.cigna.com", "/ProviderDirectory/v1/")
# endpoint_centene = Endpoint("Centene", "production.api.centene.com", "/fhir/providerdirectory/", False)
# endpoint_pacificsource = Endpoint("Pacific Source", "api.apim.pacificsource.com", "/fhir/provider/R4/")

#######################################

newconfig = configparser.ConfigParser() #create a configParser object

for endpoint in endpoints: #loop through our endpoints
    newconfig.add_section(endpoint.get("name")) #add a section for that endpoint
    newconfig.set(endpoint.get("name"), "name", endpoint.get("name")) #add it's corresponding data
    newconfig.set(endpoint.get("name"), "host", endpoint.get("host"))
    newconfig.set(endpoint.get("name"), "address", endpoint.get("address"))
    newconfig.set(endpoint.get("name"), "ssl", endpoint.get("ssl"))

print(f"CWD: {os.getcwd()}")

with open('fhirtypepkg/config/Endpoints.ini', 'w+') as configfile:
    newconfig.write(configfile)

# reader = configparser.ConfigParser()

# reader.read_file(open('Endpoints.ini', 'r'))
# sections = reader.sections()

# for section in sections:
#     print(section)

# print("Humana's hostname: ", reader["Humana"]["host"])

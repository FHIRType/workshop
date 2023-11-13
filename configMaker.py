import configparser
import json

#Create a ConfigParser object
config = configparser.ConfigParser()

#Add a section for API endpoints
config.add_section('APIEndpoints')

#List of API endpoints
endpoints = [
    {'name': 'Humana', 'host': 'fhir.humana.com', 'address': '/sandbox/api/', 'ssl': 'False'},
        {'name': 'Kaiser', 'host': 'kpx-service-bus.kp.org', 'address': '/service/hp/mhpo/healthplanproviderv1rc/', 'ssl': 'False'},
        {'name': 'Cigna', 'host': 'p-hi2.digitaledge.cigna.com', 'address': '/ProviderDirectory/v1/', 'ssl': 'False'},
        {'name': 'Centene', 'host': 'production.api.centene.com', 'address': '/fhir/providerdirectory/', 'ssl': 'False'},
        {'name': 'Pacificsource', 'host': 'api.apim.pacificsource.com', 'address': '/fhir/provider/R4/', 'ssl': 'False'}
]

# endpoint_humana = Endpoint("Humana", "fhir.humana.com", "/sandbox/api/")  # Or "/api/"
# endpoint_kaiser = Endpoint("Kaiser", "kpx-service-bus.kp.org", "/service/hp/mhpo/healthplanproviderv1rc/")
# endpoint_cigna = Endpoint("Cigna", "p-hi2.digitaledge.cigna.com", "/ProviderDirectory/v1/")
# endpoint_centene = Endpoint("Centene", "production.api.centene.com", "/fhir/providerdirectory/", False)
# endpoint_pacificsource = Endpoint("Pacific Source", "api.apim.pacificsource.com", "/fhir/provider/R4/")

# Possibly silly way to do it. I was struggling to figure out a way to add each endpoint into a config file as a seperate instance of a similiar object so that we could loop through them. 
# My solution is to turn each one into a json string object, that way it allows me to add them to a config file, since a config file needs "key:value" pairs.
for i, endpoint_info in enumerate(endpoints, start=1):
    config.set('APIEndpoints', f'Endpoint{i}', json.dumps(endpoint_info))

# Write the configuration to a file
with open('SmartClient.ini', 'w') as configfile:
    config.write(configfile)

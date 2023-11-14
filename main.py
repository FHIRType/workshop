# Authors: Iain Richey, Trenton Young, Kevin Carman, Hla Htun
# Description: Much of the functionality borrowed from code provided by Kevin.

import json
import configparser
from endpoint import Endpoint
from client import SmartClient
from standardize import getKaiserData, getHumanaData

reader = configparser.ConfigParser()

reader.read_file(open('Endpoints.ini', 'r'))
sections = reader.sections()

endpoints = []
for section in sections: #loop through each endpoint in our config and initialize it as a endpoint in a usable array
    endpoints.append(Endpoint(reader.get(section, "name"), reader.get(section, "host"), reader.get(section, "address"), reader.getboolean(section, "ssl")))


endpoint_humana = Endpoint("Humana", "fhir.humana.com", "/sandbox/api/")  # Or "/api/"
endpoint_kaiser = Endpoint("Kaiser", "kpx-service-bus.kp.org", "/service/hp/mhpo/healthplanproviderv1rc/")
endpoint_cigna = Endpoint("Cigna", "p-hi2.digitaledge.cigna.com", "/ProviderDirectory/v1/")
endpoint_centene = Endpoint("Centene", "production.api.centene.com", "/fhir/providerdirectory/", False)
endpoint_pacificsource = Endpoint("Pacific Source", "api.apim.pacificsource.com", "/fhir/provider/R4/")

# endpoints = [
#     endpoint_humana,
#     endpoint_centene,
#     endpoint_cigna,
#     endpoint_kaiser,
#     endpoint_pacificsource
# ]

# +19087212277 <- ideal
# def somefunc(oldphonenumber):
#     return "fixed phone number"
# endpoint_pacificsource.set_mask(endpoint_pacificsource.get_location_str()+"_phonenumber", lambda oldphonenumber : somefunc(oldphonenumber))
# badphone = "+(1212)334313"
# print(endpoint_pacificsource.use_mask(endpoint_pacificsource.get_location_str()+"_phonenumber", badphone))

provider_lookup_name_data = [
    # {"f_name": "Brandon", "l_name": "Bianchini", "NPI": "1700158326", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    {"f_name": "Kaydie", "l_name": "Satein", "NPI": "1619302171", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Toren", "l_name": "Davis", "NPI": "1457779498", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Marilyn", "l_name": "Darr", "NPI": "1902844418", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "David", "l_name": "Ruiz", "NPI": "1508803982", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Olivia", "l_name": "Wright", "NPI": "1205876182", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "John", "l_name": "Nusser", "NPI": "1467549204", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Melinda", "l_name": "Landchild", "NPI": "1992743546", "prac_resp": "None", "prac_role_resp": "None",
     "loc_resp": "None"},
    {"f_name": "Natasha", "l_name": "Ingvoldstad-O'Neal", "NPI": "1689871147", "prac_resp": "None",
     "prac_role_resp": "None", "loc_resp": "None"},
    # {"f_name": "Michael", "l_name": "Liu", "NPI": "1841210549", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "David", "l_name": "Paik", "NPI": "1023218047", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"},
    # {"f_name": "Adriana", "l_name": "Linares", "NPI": "1558577130", "prac_resp": "None", "prac_role_resp": "None",
    #  "loc_resp": "None"}
]


def print_resource(resource):
    """
    This function converts our resource into a json, then prints it. seems a lot of the class functions return data that is
    in JSON format but needs to be converted first
    """

    print(json.dumps(resource.as_json(), sort_keys=False, indent=2))


def print_res_obj(obj):
    for res in obj:
        print(res, ": ", obj[res])
    print("\n")


def main():
    # TODO: Initialize these concurrently, the requests should all be sent at the same time - perhaps use asyncio? (iain)
    smartClients = []
    for endpoint in endpoints:
        # endpoint.print_info()
        smartClients.append(SmartClient(endpoint))

    # smartclient_humana = SmartClient(endpoint_humana)
    # smartclient_centene = SmartClient(endpoint_centene)
    # smartclient_cigna = SmartClient(endpoint_cigna)
    # smartclient_kaiser = SmartClient(endpoint_kaiser)
    # smartclient_pacificsource = SmartClient(endpoint_pacificsource)

    # clients = [
    #     smartclient_humana,
    #     smartclient_centene,
    #     smartclient_cigna,
    #     smartclient_kaiser,
    #     smartclient_pacificsource
    #              ]

    # for _client in clients:
    #     req = "metadata"
    #     query = "GET " + _client.get_endpoint_url() + req
    #     print(query, _client.http_query(req), sep=" | ")

    for client in smartClients:
        print("\n  ####  ", client.get_endpoint_name(), "  ####")
        print("\nProvider Data\n")
        for data in provider_lookup_name_data:
            resource = client.find_practitioner(data["f_name"], data["l_name"], data["NPI"])
            if resource:
                # print_resource(resource)
                if client.get_endpoint_name() == "Humana":
                    print_res_obj(getHumanaData(resource))
                elif client.get_endpoint_name() == "Kaiser":
                    print_res_obj(getKaiserData(resource))
        else:
            print("...", end="")


if __name__ == "__main__":
    main()


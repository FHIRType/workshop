import csv
import os
import json
from math import cos, sqrt, asin
import requests

KEY = "ke8tKKYvB480ZEEtJY9cPfNxW85yWKs0"

class mapQuest:
    def __init__(self):
        self.key = KEY
        self.endpoint = "https://www.mapquestapi.com/geocoding/v1/address"

    def geocode(self, location):
        params = {
            "key": self.key,
            "location": location
        }
        response = requests.get(self.endpoint, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        
        return response.json().get("results")[0].get("locations")[0].get("latLng")

def Hav_distance(lat1, lon1, lat2, lon2):
    r = 6371 # radius of earth in km
    p = 0.017453292519943295  #Pi/180

    Lat1 = float(lat1)
    Lon1 = float(lon1)
    Lat2 = float(lat2)
    Lon2 = float(lon2)

    a = 0.5 - cos((Lat2-Lat1)*p)/2 + cos(Lat1*p)*cos(Lat2*p) * (1-cos((Lon2-Lon1)*p)) / 2
    d = 2 * r * asin(sqrt(a)) #2*R*asin

    #print("distance between ", Lat1, Lon1, " and ", Lat2, Lon2, " is ", d)

    return d

def rec_match(rec1, rec2):
    if rec1['NPI'] != rec2['NPI']:
        return 0
    
    if rec1['Taxonomy'] != rec2['Taxonomy']:
        #TODO optional peramitor for ignoring Taxonomy 
        #If environment variable set = test dont call mapquest probably read from env file
        return 0

    if rec1['State'] != rec2['State']:
        return 0
    
    if rec1['City'] != rec2['City']:
        return 0

    if rec1['Zip'] != rec2['Zip']: #change this to check first 5?
        return 0

    Map = mapQuest()
    addr1 = Map.geocode(rec1['ADD1'] + ", " + rec1['City'] + rec1['State'] + ", " + rec1['Zip'])
    addr2 = Map.geocode(rec2['ADD1'] + ", " + rec2['City'] + rec2['State'] + ", " + rec2['Zip'])

    if Hav_distance(addr1['lat'], addr1['lng'], addr2['lat'], addr2['lng']) > 10:
        return 0
    
    return 1

def group_rec(recs):
    groups = []
    for rec in recs:
        if len(groups) == 0:
            groups.append([rec])
            continue
        for group in groups:
            if rec_match(group[0], rec):
                group.append(rec)
                break
        else:
            groups.append([rec])
    return groups

input = [
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Jerry", 'NPI': "1134523127", 'FirstName': "Jerry",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "104T00000X", 'GroupName': "Jerry Bones Emp", 'ADD1': "472 Kneecap Drive", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "1345837645", 'Fax': "1039273645", 'Email': "Bones@wackycracky.net", 'lat': "45.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Lost, Garry", 'NPI': "1134523127", 'FirstName': "Gary",
        'LastName': "Lost", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Ripoff Emporium", 'ADD1': "398 Cheapskate Lane", 'ADD2': "", 'City': "Conman City",
        'State': "LI", 'Zip': "000000000", 'Phone': "9873640918", 'Fax': "1090283647", 'Email': "Cheat@hotmail.com", 'lat': "84.2313", 'lng': "646.4531"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    }
]

input1 = [
        {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Lost, Garry", 'NPI': "1134523127", 'FirstName': "Gary",
        'LastName': "Lost", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Ripoff Emporium", 'ADD1': "2370 West 21st Street", 'ADD2': "", 'City': "Eugene",
        'State': "OR", 'Zip': "000000000", 'Phone': "9873640918", 'Fax': "1090283647", 'Email': "Cheat@hotmail.com", 'lat': "84.2313", 'lng': "646.4531"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "1218 NW 23rd Street", 'ADD2': "", 'City': "Corvallis",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "1218 NW 23rd Street", 'ADD2': "", 'City': "Corvallis",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    }
]

if __name__ == "__main__":
    Map = mapQuest()

    # test1 = Map.geocode("001 4th Ave., Kooskia ID, 835390339")
    # test2 = Map.geocode("001 4th Ave., Kooskia ID, 83539")
    # print(Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng']))

    # test1 = Map.geocode("00018 County Rd 1030 Ste 125, Frisco CO, 80443")
    # test2 = Map.geocode("0038 County Rd Ste 1030, Frisco CO, 80443")
    # print(Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng']))

    # test1 = Map.geocode("0310 County Road Ste 14, Del Norte CO, 811328719")
    # test2 = Map.geocode("0310 County Road Ste 14, Del Norte CO, 81132")
    # print(Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng']))
          	                                        

    # test1 = Map.geocode("1 Barnes Jewish Hospital Plaza St, Saint Louis MO,	631101003")
    # test2 = Map.geocode("1 Barnes Jewish Hospital Plaza, Saint Louis MO, 631101003")
    # print(Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng']))

    match_test = group_rec(input1)

    for match in match_test:
        print(match)
        print()





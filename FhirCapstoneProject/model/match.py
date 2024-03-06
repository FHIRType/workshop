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

    print("distance between ", Lat1, Lon1, " and ", Lat2, Lon2, " is ", d)

def rec_match(addr1, addr2):
    if addr1['State'] != addr2['State']:
        return 0
    
    if addr1['City'] != addr2['City']:
        return 0

    if addr1['zip'] != addr2['zip']: #change this to check first 5?
        return 0
    
    #TODO: add address matching once it is figured out 

    return 1
    
if __name__ == "__main__":
    Map = mapQuest()

    test1 = Map.geocode("001 4th Ave., Kooskia ID, 835390339")
    test2 = Map.geocode("001 4th Ave., Kooskia ID, 83539")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])

    test1 = Map.geocode("00018 County Rd 1030 Ste 125, Frisco CO, 80443")
    test2 = Map.geocode("0038 County Rd Ste 1030, Frisco CO, 80443")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])

    test1 = Map.geocode("0310 County Road Ste 14, Del Norte CO, 811328719")
    test2 = Map.geocode("0310 County Road Ste 14, Del Norte CO, 81132")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])
          	                                        

    test1 = Map.geocode("1 Barnes Jewish Hospital Plaza St, Saint Louis MO,	631101003")
    test2 = Map.geocode("1 Barnes Jewish Hospital Plaza, Saint Louis MO, 631101003")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])

    test1 = Map.geocode("1 12th St, Ste 4, Astoria OR,	971034146")
    test2 = Map.geocode("1 12th St Ste 4, Astoria OR, 971034146")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])

    test1 = Map.geocode("1218 NW 23rd St, Corvallis OR,	97330")
    test2 = Map.geocode("2310 NW Hayes Ave, Corvallis OR, 97330")
    Hav_distance(test1['lat'], test1['lng'], test2['lat'], test2['lng'])
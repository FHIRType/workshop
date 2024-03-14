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
    if rec1['lat'] == "" or rec1['lng'] == "":
        addr1 = Map.geocode(rec1['ADD1'] + ", " + rec1['City'] + rec1['State'] + ", " + rec1['Zip'])
        rec1['lat'] = addr1['lat']
        rec1['lng'] = addr1['lng']

    if rec2['lat'] == "" or rec2['lng'] == "":
        addr2 = Map.geocode(rec2['ADD1'] + ", " + rec2['City'] + rec2['State'] + ", " + rec2['Zip'])
        rec2['lat'] = addr2['lat']
        rec2['lng'] = addr2['lng']

    if Hav_distance(rec1['lat'], rec1['lng'], rec2['lat'], rec2['lng']) > 10:
        return 0
    
    return 1


def group_rec(recs):
    """
    Groups endpoint responses based on similarity of the responses.

    If two responses share NPI, taxonomy, zip, and are within a margin of distance of each other, they will be grouped together

    :param parameters: a list of responses (dicts)
    :return: A list of lists of dicts
    """
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


if __name__ == "__main__":
    Map = mapQuest()

    # match_test = group_rec(input)

    # for match in match_test:
    #     print(match)
    #     print()





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
        """
        Takes in a street address, sends that address to the mapquest API, and returns the latitude and longitude
        """
        params = {
            "key": self.key,
            "location": location
        }
        response = requests.get(self.endpoint, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        
        return response.json().get("results")[0].get("locations")[0].get("latLng")

def Hav_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the haversine distance between two coordinates. The Haversine formula is the distance
    between two points on a sphere, meaning it accounts for curvature. It is just a way for us 
    to find the true distance between two lat long pairs
    """
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
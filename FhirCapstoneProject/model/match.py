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
    if rec1['lat'] == "" or rec1['lng'] == "" or rec1['lat'] is None or rec1['lng'] is None:
        addr1 = Map.geocode(rec1['ADD1'] + ", " + rec1['City'] + rec1['State'] + ", " + rec1['Zip'])
        rec1['lat'] = addr1['lat']
        rec1['lng'] = addr1['lng']

    if rec2['lat'] == "" or rec2['lng'] == "" or rec2['lat'] is None or rec2['lng'] is None:
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

    match_input = [
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:07:05Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:26:02Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T08:53:45Z",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:10Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:07:05Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:26:02Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T10:16:17Z",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:10Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:07:05Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:26:02Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T12:07:47Z",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:10Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:07:05Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:26:02Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T17:30:40Z",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:10Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:07:05Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:26:02Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T05:31:10Z",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:10Z"
        },
        {
            "Endpoint": "Kaiser",
            "DateRetrieved": "2024-03-13T23:07:12Z",
            "Accuracy": -1,
            "FullName": "Dykstra, Michelle L",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2024-03-12T00:27:02-07:00",
            "GroupName": "Willamette Valley Family Center, LLC",
            "Taxonomy": None,
            "LastPracRoleUpdate": "2024-03-12T00:55:23-07:00",
            "ADD1": "610 Jefferson St",
            "ADD2": "Optional",
            "City": "Oregon City",
            "State": "OR",
            "Zip": "97045-2329",
            "Phone": 8556328280,
            "Fax": 5036577676,
            "Email": None,
            "lat": 45.354828,
            "lng": -122.604025,
            "LastLocationUpdate": "2024-03-12T00:06:18-07:00"
        },
        {
            "Endpoint": "Cigna",
            "DateRetrieved": "2024-03-13T23:07:13Z",
            "Accuracy": -1,
            "FullName": "DYKSTRA, MICHELLE",
            "NPI": 1013072586,
            "FirstName": "Michelle",
            "LastName": "Dykstra",
            "Gender": "Female",
            "LastPracUpdate": "2023-09-01T23:30:35Z",
            "GroupName": None,
            "Taxonomy": "103T00000X",
            "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
            "ADD1": "610 JEFFERSON ST",
            "ADD2": "Optional",
            "City": "OREGON CITY",
            "State": "OR",
            "Zip": "97045-2329",
            "Phone": 5036577235,
            "Fax": None,
            "Email": None,
            "lat": 45.3403,
            "lng": -122.5778,
            "LastLocationUpdate": "2023-09-12T23:46:56Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:08:34Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2023-08-06T08:18:52Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T12:09:51Z",
            "ADD1": "8280 Ne Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124",
            "Phone": 5034399531,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:13:27Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:08:34Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2023-08-06T08:18:52Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T07:10:53Z",
            "ADD1": "8280 Ne Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124",
            "Phone": 5034399531,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:13:27Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:08:34Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2023-08-06T08:18:52Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T13:49:57Z",
            "ADD1": "8280 Ne Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124",
            "Phone": 5034399531,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:13:27Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:08:34Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2023-08-06T08:18:52Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T17:34:11Z",
            "ADD1": "8280 Ne Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124",
            "Phone": 5034399531,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:13:27Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:08:34Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2023-08-06T08:18:52Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T10:06:08Z",
            "ADD1": "8280 Ne Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124",
            "Phone": 5034399531,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:13:27Z"
        },
        {
            "Endpoint": "Kaiser",
            "DateRetrieved": "2024-03-13T23:08:39Z",
            "Accuracy": -1,
            "FullName": "Vincent, Steven",
            "NPI": 1053483933,
            "FirstName": "Steven",
            "LastName": "Vincent",
            "Gender": "Male",
            "LastPracUpdate": "2024-03-12T00:17:12-07:00",
            "GroupName": "Western Psychological & Counseling - Hillsboro",
            "Taxonomy": None,
            "LastPracRoleUpdate": "2024-03-12T00:51:53-07:00",
            "ADD1": "8280 NE Mauzey Ct",
            "ADD2": "Optional",
            "City": "Hillsboro",
            "State": "OR",
            "Zip": "97124-9092",
            "Phone": 9718083665,
            "Fax": None,
            "Email": None,
            "lat": 45.566849,
            "lng": -122.895479,
            "LastLocationUpdate": "2024-03-12T02:26:12-07:00"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:10:01Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:21:25Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T13:56:26Z",
            "ADD1": "945 11th Ave",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632",
            "Phone": 3604148600,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:23Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:10:01Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:21:25Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T17:48:46Z",
            "ADD1": "945 11th Ave",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632",
            "Phone": 3604148600,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:23Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:10:01Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:21:25Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T16:26:25Z",
            "ADD1": "945 11th Ave",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632",
            "Phone": 3604148600,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:23Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:10:01Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:21:25Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T11:44:50Z",
            "ADD1": "945 11th Ave",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632",
            "Phone": 3604148600,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:23Z"
        },
        {
            "Endpoint": "Humana",
            "DateRetrieved": "2024-03-13T23:10:01Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2023-08-06T08:21:25Z",
            "GroupName": None,
            "Taxonomy": None,
            "LastPracRoleUpdate": "2023-08-05T05:37:47Z",
            "ADD1": "945 11th Ave",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632",
            "Phone": 3604148600,
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastLocationUpdate": "2023-08-06T08:12:23Z"
        },
        {
            "Endpoint": "Kaiser",
            "DateRetrieved": "2024-03-13T23:10:06Z",
            "Accuracy": -1,
            "FullName": "Smith, Fran J",
            "NPI": 1215022546,
            "FirstName": "Fran",
            "LastName": "Smith",
            "Gender": "Female",
            "LastPracUpdate": "2024-03-12T00:25:28-07:00",
            "GroupName": "Northwest Psychological Resources, LLC",
            "Taxonomy": None,
            "LastPracRoleUpdate": "2024-03-12T00:55:20-07:00",
            "ADD1": "945 11th Ave Ste B",
            "ADD2": "Optional",
            "City": "Longview",
            "State": "WA",
            "Zip": "98632-2555",
            "Phone": 8556328280,
            "Fax": 3606367372,
            "Email": None,
            "lat": 46.130493,
            "lng": -122.934228,
            "LastLocationUpdate": "2024-03-13T09:20:29-07:00"
        }
    ]

    match_test = group_rec(match_input)

    print(match_test)

    # for match in match_test:
    #     print(match)
    #     print()





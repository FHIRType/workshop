import csv
import os
from json import loads, dumps
from math import cos, sqrt, asin, pi
import requests

KEY = os.environ.get("MAPQUEST_API_KEY")


class MapQuest:
    """
    Overview
    --------
    Class to facilitate easy connection and communication with the MapQuest API. Expects a environment variable 
    called MAPQUEST_API_KEY to be set in order to use the API. 

    Upon initialization: sets the key for the API and the endpoint for the API.

    Attributes
    -----------
    endpoint
        Holds the endpoint we are connecting to at mapquest

    key
        Holds the key for the API
    """
    def __init__(self):
        self.key = KEY
        self.endpoint = "https://www.mapquestapi.com/geocoding/v1/address"

    def geocode(self, location):
        """
        Function to connect to the mapquest api and get the lat long of the location

        :param queries: location to geocode
        :return: The lat long pairing of the location
        """
        params = {"key": self.key, "location": location}
        response = requests.get(self.endpoint, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        return response.json().get("results")[0].get("locations")[0].get("latLng")


def hav_distance(lat1, lon1, lat2, lon2):
    """
    Function to find the true distance between two locations based off of the earths curve

    :param queries: two lat long pairings
    :return: distance between the two
    """
    r = 6371  # radius of earth in km
    p = pi / 180

    Lat1 = float(lat1)
    Lon1 = float(lon1)
    Lat2 = float(lat2)
    Lon2 = float(lon2)

    a = (
        0.5
        - cos((Lat2 - Lat1) * p) / 2
        + cos(Lat1 * p) * cos(Lat2 * p) * (1 - cos((Lon2 - Lon1) * p)) / 2
    )
    d = 2 * r * asin(sqrt(a))  # 2*R*asin

    return d


def rec_match(rec1, rec2, use_taxonomy):
    """
    A model to match two records based off of NPI, Taxonomy (if the flag is on), State, City, and Zip.
    Use this model to group records together based on if they are the same practitioner at the same location or not. 

    :param queries: Two records, and a flag to use taxonomy
    :return: Boolean value for if they are the same or not
    """
    if rec1["NPI"] != rec2["NPI"]:
        return 0

    if use_taxonomy:
        if rec1["Taxonomy"] != rec2["Taxonomy"]:
            # TODO optional parameter for ignoring Taxonomy
            # If environment variable set = test dont call mapquest probably read from env file

            return 0

    if rec1["State"] != rec2["State"]:
        return 0

    if rec1["City"] != rec2["City"]:
        return 0

    if rec1["Zip"][:5] != rec2["Zip"][:5]: 
        return 0

    Map = MapQuest()

    # Compare the geocodes of rec1 and rec2
    if (
        rec1["lat"] == ""
        or rec1["lng"] == ""
        or rec1["lat"] is None
        or rec1["lng"] is None
    ):
        addr1 = Map.geocode(
            rec1["ADD1"] + ", " + rec1["City"] + rec1["State"] + ", " + rec1["Zip"]
        )
        rec1["lat"] = addr1["lat"]
        rec1["lng"] = addr1["lng"]

    if (
        rec2["lat"] == ""
        or rec2["lng"] == ""
        or rec2["lat"] is None
        or rec2["lng"] is None
    ):
        addr2 = Map.geocode(
            rec2["ADD1"] + ", " + rec2["City"] + rec2["State"] + ", " + rec2["Zip"]
        )
        rec2["lat"] = addr2["lat"]
        rec2["lng"] = addr2["lng"]

    if hav_distance(rec1["lat"], rec1["lng"], rec2["lat"], rec2["lng"]) > 10:
        return 0

    return 1


def group_rec(recs: list[dict], use_taxonomy: bool):
    """
    Groups endpoint responses based on similarity of the responses.

    If two responses share NPI, taxonomy, zip, and are within a margin of distance of each other, they will be grouped together

    :param recs: a list of responses (dicts)
    :return: A list of lists of dicts
    """
    groups = []
    for rec in recs:
        if len(groups) == 0:
            groups.append([rec])
            continue
        for group in groups:
            if rec_match(group[0], rec, use_taxonomy):
                group.append(rec)
                break
        else:
            groups.append([rec])
    return groups

match_input = [
     {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Jerry",
        "NPI": "1134523127",
        "FirstName": "Jerry",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Jerry Bones Emp",
        "ADD1": "472 Kneecap Drive",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "1345837645",
        "Fax": "1039273645",
        "Email": "Bones@wackycracky.net",
        "lat": "45.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Lost, Garry",
        "NPI": "1134523127",
        "FirstName": "Gary",
        "LastName": "Lost",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Ripoff Emporium",
        "ADD1": "398 Cheapskate Lane",
        "ADD2": "",
        "City": "Conman City",
        "State": "LI",
        "Zip": "000000000",
        "Phone": "9873640918",
        "Fax": "1090283647",
        "Email": "Cheat@hotmail.com",
        "lat": "84.2313",
        "lng": "646.4531",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Johnny Bones Emporium",
        "ADD1": "676 Femur Lane",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "3239078654",
        "Fax": "1739216345",
        "Email": "Bones@achybreaky.com",
        "lat": "63.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Jerry",
        "NPI": "1134523127",
        "FirstName": "Jerry",
        "LastName": "Bones",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Jerry Bones Emp",
        "ADD1": "472 Kneecap Drive",
        "ADD2": "",
        "City": "Imperium City",
        "State": "OR",
        "Zip": "970454523",
        "Phone": "1345837645",
        "Fax": "1039273645",
        "Email": "Bones@wackycracky.net",
        "lat": "45.35497",
        "lng": "-213.60343",
    },
    {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Lost, Garry",
        "NPI": "1134523127",
        "FirstName": "Gary",
        "LastName": "Lost",
        "Gender": "M",
        "Taxonomy": "103T00000X",
        "GroupName": "Ripoff Emporium",
        "ADD1": "398 Cheapskate Lane",
        "ADD2": "",
        "City": "Conman City",
        "State": "LI",
        "Zip": "000000000",
        "Phone": "9873640918",
        "Fax": "1090283647",
        "Email": "Cheat@hotmail.com",
        "lat": "84.2313",
        "lng": "646.4531",
    }
]

if __name__ == "__main__":
    json_string = group_rec(match_input, False)
    output_dict = loads(dumps(json_string))

    print (output_dict)
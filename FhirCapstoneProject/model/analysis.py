# Authors: Iain Richey, Hla Htun
####################
# This file contains the different analysis models for the different types of queries
####################
from datetime import datetime as dtime

import numpy as np


####################
# This function takes in a set of queries to the various endpoints, and analyses them for the most likely results
####################


def predict(queries) -> dict:  # will return whatever our container class is
    """
    Our main prediction model. It takes in a list of endpoint responses, and builds the
    most accurate prediction from them. This works by applying a weight to each response
    based on the update date for the response, using the logit function. Then, each endpoint
    'votes' on the value of feature using this weight. The highest voted value for each key is then
    used in the final output response.

    :param queries: a list of endpoint responses
    :return: Dict object of the predicted tuple
    """
    unique_features = {}
    today = dtime.today()
    for query in queries:  # loop through each endpoints query

        if len(queries) == 0:
            return queries[0].id, queries

        max_fea = {}
        last_updated_str = query.get("LastPracUpdate", "")

        try:
            last_updated = dtime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            last_updated = dtime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S%z")

        if not last_updated:
            continue

        time_diff = (today.date() - last_updated.date()).days

        time_diff /= 100

        if query != None:  # some endpoints might not have the person

            # matches unique features (ie no repeats)
            for index, (key, value) in enumerate(query.items()):

                if key not in unique_features:  # add each unique feature to our dict
                    unique_features[key] = {}

                    if value != None:  # make sure we aren't including nulls
                        if value in unique_features[key]:
                            unique_features[key][value] += time_diff

                        else:
                            unique_features[key][value] = time_diff

    highest_features = {
        feature: max(options, key=options.get) if options else None
        for feature, options in unique_features.items()
    }

    highest_features["Accuracy"] = 1
    highest_features["Endpoint"] = "Consensus"

    return highest_features


def logistic(last_updated):
    return 1 / (1 + np.exp(-last_updated))


input = [
    {
        "Endpoint": "Kiaser",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        "LastPracUpdate": "2021-06-22T11:03:51Z",
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
        "Endpoint": "Centene",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        "LastPracUpdate": "2021-06-22T11:03:51Z",
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
        "Endpoint": "Humana",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Johnny",
        "NPI": "1134523127",
        "FirstName": "Johnny",
        "LastName": "Bones",
        "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        "LastPracUpdate": "2021-06-22T11:03:51Z",
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
        "Endpoint": "Humana",
        "DateRetrieved": "2/1/2024",
        "FullName": "Bones, Jerry",
        "NPI": "1134523127",
        "FirstName": "Jerry",
        "LastName": "Bones",
        "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        "LastPracUpdate": "2021-06-22T11:03:51Z",
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
        "Endpoint": "Kaiser",
        "DateRetrieved": "2/1/2024",
        "FullName": "Lost, Garry",
        "NPI": "1134523127",
        "FirstName": "Gary",
        "LastName": "Lost",
        "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        "LastPracUpdate": "2021-06-22T11:03:51Z",
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
]

if __name__ == "__main__":
    consensus = predict(input)

    print(consensus)

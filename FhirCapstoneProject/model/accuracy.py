# Authors: Iain Richey
# Description: contains the current accuracy model we are using

from json import loads, dumps


def calc_accuracy(ep_responses: list, model_output: dict) -> list:
    """
    Calculates the accuracy score of endpoint responses to a specific query, based off
    of the analysis model output.

    Calculation is based off of how many elements an endpoint output shared with the anaylsis model output divided by total number

    :param parameters: A list of dicts (endpoint responses) and a dict that is the output of our model.
    :return: The resulting list of flattened data, now with an accuracy score on each.
    """
    acc_output = ep_responses
    query_num = 0
    for query in acc_output:  # loop through each endpoint query
        query_num += 1
        if query is not None:  # some endpoints might not have the person

            # matches unique features (ie no repeats)
            acc_score = 0
            for index, (key, value) in enumerate(query.items()):
                if value == model_output[key] and key != "Endpoint":
                    acc_score += 1

            query["Accuracy"] = round(
                acc_score / (len(model_output) - 1), 2
            )  # -1 for endpoint

    return acc_output

accuracy_input = [
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
]


accuracy_consensus = {'Endpoint': 'Consensus', 'DateRetrieved': '2/1/2024', 
                   'FullName': 'Bones, Johnny', 'NPI': '1134523127', 
                   'FirstName': 'Johnny', 'LastName': 'Bones', 
                   'LastPracRoleUpdate': '2023-11-09T03:23:38Z', 
                   'LastPracUpdate': '2021-06-22T11:03:51Z', 'Gender': 'M', 
                   'Taxonomy': '103T00000X', 
                   'GroupName': 'Johnny Bones Emporium', 
                   'ADD1': '676 Femur Lane', 'ADD2': '', 
                   'City': 'Imperium City', 'State': 'OR', 
                   'Zip': '970454523', 'Phone': '3239078654', 
                   'Fax': '1739216345', 'Email': 'Bones@achybreaky.com', 
                   'lat': '63.35497', 'lng': '-213.60343', 'Accuracy': 1}

if __name__ == "__main__":
    json_string = calc_accuracy(accuracy_input, accuracy_consensus)
    output_dict = loads(dumps(json_string))
    
    print(output_dict)
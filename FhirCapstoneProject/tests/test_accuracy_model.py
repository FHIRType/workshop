# Authors: Iain Richey
# Description: Tests the accuracy model 
from FhirCapstoneProject.model.accuracy import calc_accuracy
import pytest
from json import loads
from deepdiff import DeepDiff

@pytest.fixture
def analysis_prediction():
    concencus = {
            'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Dykstra, Michelle L.", 'NPI': "1013072586", 'FirstName': "Michelle",
            'LastName': "Dykstra", 'Gender': "F", 'Taxonomy': "103T00000X", 'GroupName': "Willamette Valley Family Center", 'ADD1': "610 Jefferson St", 'ADD2': "", 'City': "Oregon City",
            'State': "OR", 'Zip': "970452329", 'Phone': "5036577235", 'Fax': "5036577676", 'Email': "BILLING@WVFC.NET", 'lat': "45.35497", 'lng': "-122.60343"
        }
    return concencus

@pytest.fixture
def expected_input():
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
            'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Jerry Bones Emp", 'ADD1': "472 Kneecap Drive", 'ADD2': "", 'City': "Imperium City",
            'State': "OR", 'Zip': "970454523", 'Phone': "1345837645", 'Fax': "1039273645", 'Email': "Bones@wackycracky.net", 'lat': "45.35497", 'lng': "-213.60343"
        },
        {
            'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Lost, Garry", 'NPI': "1134523127", 'FirstName': "Gary",
            'LastName': "Lost", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Ripoff Emporium", 'ADD1': "398 Cheapskate Lane", 'ADD2': "", 'City': "Conman City",
            'State': "LI", 'Zip': "000000000", 'Phone': "9873640918", 'Fax': "1090283647", 'Email': "Cheat@hotmail.com", 'lat': "84.2313", 'lng': "646.4531"
        }
    ]
    return input

def test_accuracy_model(expected_input, analysis_prediction):
    output = [
        {"Endpoint": "", "DateRetrieved": "2/1/2024", "FullName": "Bones, Johnny", "NPI": "1134523127", "FirstName": "Johnny", "LastName": "Bones", "Gender": "M", "Taxonomy": "103T00000X", "GroupName": "Johnny Bones Emporium", "ADD1": "676 Femur Lane", "ADD2": "", "City": "Imperium City", "State": "OR", "Zip": "970454523", "Phone": "3239078654", "Fax": "1739216345", "Email": "Bones@achybreaky.com", "lat": "63.35497", "lng": "-213.60343", "acc_score": 0.22}, 
        {"Endpoint": "", "DateRetrieved": "2/1/2024", "FullName": "Bones, Johnny", "NPI": "1134523127", "FirstName": "Johnny", "LastName": "Bones", "Gender": "M", "Taxonomy": "103T00000X", "GroupName": "Johnny Bones Emporium", "ADD1": "676 Femur Lane", "ADD2": "", "City": "Imperium City", "State": "OR", "Zip": "970454523", "Phone": "3239078654", "Fax": "1739216345", "Email": "Bones@achybreaky.com", "lat": "63.35497", "lng": "-213.60343", "acc_score": 0.22}, 
        {"Endpoint": "", "DateRetrieved": "2/1/2024", "FullName": "Bones, Johnny", "NPI": "1134523127", "FirstName": "Johnny", "LastName": "Bones", "Gender": "M", "Taxonomy": "103T00000X", "GroupName": "Johnny Bones Emporium", "ADD1": "676 Femur Lane", "ADD2": "", "City": "Imperium City", "State": "OR", "Zip": "970454523", "Phone": "3239078654", "Fax": "1739216345", "Email": "Bones@achybreaky.com", "lat": "63.35497", "lng": "-213.60343", "acc_score": 0.22}, 
        {"Endpoint": "", "DateRetrieved": "2/1/2024", "FullName": "Bones, Jerry", "NPI": "1134523127", "FirstName": "Jerry", "LastName": "Bones", "Gender": "M", "Taxonomy": "103T00000X", "GroupName": "Jerry Bones Emp", "ADD1": "472 Kneecap Drive", "ADD2": "", "City": "Imperium City", "State": "OR", "Zip": "970454523", "Phone": "1345837645", "Fax": "1039273645", "Email": "Bones@wackycracky.net", "lat": "45.35497", "lng": "-213.60343", "acc_score": 0.28}, 
        {"Endpoint": "", "DateRetrieved": "2/1/2024", "FullName": "Lost, Garry", "NPI": "1134523127", "FirstName": "Gary", "LastName": "Lost", "Gender": "M", "Taxonomy": "103T00000X", "GroupName": "Ripoff Emporium", "ADD1": "398 Cheapskate Lane", "ADD2": "", "City": "Conman City", "State": "LI", "Zip": "000000000", "Phone": "9873640918", "Fax": "1090283647", "Email": "Cheat@hotmail.com", "lat": "84.2313", "lng": "646.4531", "acc_score": 0.17}]
    return output

    json_string = calc_accuracy(expected_input, analysis_prediction)
    output_dict = loads(json_string)

    diff = DeepDiff(output_dict, output) 

    assert not diff
    
    
# Authors: Iain Richey
# Description: contains the current accuracy model we are using 

# import csv
# import os
import json

def calc_accuracy(ep_responses:list, model_output:dict) -> list:
    """
    Calculates the accuracy score of endpoint responses to a specific query, based off 
    of the analysis model output. 

    Calculation is based off of how many elements an endpoint output shared with the anaylsis model output divided by total number

    :param parameters: A list of dicts (endpoint responses) and a dict that is the output of our model. 
    :return: A json file containing the different endpoint responses with their accuracy scores
    """
    acc_output = ep_responses
    unique_features = {}
    query_num = 0   
    for query in acc_output: #loop through each endpoints query
        query_num += 1
        if query != None: #some endpoints might not have the person
        
            #matches unique features (ie no repeats)
            acc_score = 0
            for index, (key, value) in enumerate(query.items()):
                if (value == model_output[key] and key != 'Endpoint'):
                    acc_score += 1
                
            query['acc_score'] = round(acc_score/(len(model_output) -1), 2) #-1 for endpoint

    json_string = json.dumps(acc_output)        
    return json_string

    #return a JSON, make a new variable and return it 







# script_directory = os.path.dirname(os.path.abspath(__file__))
# csv_file_name = 'flat_data_example.csv'
# csv_file_path = os.path.join(script_directory, csv_file_name)

# model_output = {'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Dykstra, Michelle L.", 'NPI': "1013072586", 'FirstName': "Michelle",
#                 'LastName': "Dykstra", 'Gender': "F", 'Taxonomy': "103T00000X", 'GroupName': "Willamette Valley Family Center", 'ADD1': "610 Jefferson St", 'ADD2': "", 'City': "Oregon City",
#                 'State': "OR", 'Zip': "970452329", 'Phone': "5036577235", 'Fax': "5036577676", 'Email': "BILLING@WVFC.NET", 'lat': "45.35497", 'lng': "-122.60343"}

# with open(csv_file_path) as csv_file:
#     reader = csv.reader(csv_file, delimiter=',')

#     #get the first line for headers
#     first_row = next(reader)
#     line_count = 0

#     flattened_data = []
#     for row in reader:
#         temp_dict = {}
#         for index, value in enumerate(row):
#             temp_dict[first_row[index]] = value

#         flattened_data.append(temp_dict)
    
#     calc_accuracy(flattened_data, model_output)
# Authors: Iain Richey, Hla Htun
####################
# This file contains the different analysis models for the different types of queries
####################
from datetime import datetime as dtime
import numpy as np
from dateutil import parser

####################
# This function takes in a set of queries to the various endpoints, and analyses them for the most likely results
####################

def predict(queries) -> dict: #will return whatever our container class is 
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
    for query in queries: #loop through each endpoints query

        if len(queries) == 0:
            return queries[0].id, queries

        max_fea = {}
        for query in queries:
            last_updated = parser.parse(query.get("LastPracUpdate", ""))
            if not last_updated:
                continue

            time_diff = (today.date() - last_updated.date()).days
            
            time_diff /= 100
            if query != None: #some endpoints might not have the person

                #matches unique features (ie no repeats)
                for index, (key, value) in enumerate(query.items()):

                    if key not in unique_features: #add each unique feature to our dict
                        unique_features[key] = {}

                    if value in unique_features[key]:
                        unique_features[key][value] += time_diff

                    else: 
                        unique_features[key][value] = time_diff

    highest_features = [] #dict of the highest voted result for each feature
    highest_features = {feature: max(options, key=options.get) for feature, options in unique_features.items()}

    highest_features["Accuracy"] = 1
    highest_features["Endpoint"] = "Concensus"

    return highest_features

def logistic(last_updated):
    return 1 / (1 + np.exp(-last_updated))
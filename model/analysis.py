#Author: Iain Richey
####################
#This file ccontains the different analysis models for the different types of queries
#if you are lookin for the test of the models, they are in the other file
####################

test_data = [
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 37},
    {'fname': 'Johnny', 'lname': 'Weaver', 'npi': '123456', 'age': 22},
    {'fname': 'Iain', 'lname': 'Richey', 'npi': '137681', 'age': 37},
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 40}
]

####################
#This function takes in a set of queries to the various endpoints, and analyses them for the
# most likely results 
#
####################
def predict(queries, time_factor) -> dict: #will return whatever our container class is 
    #TODO change up params and setup depending on if the endpoints are 
    #quieried before this step, or during it 

    #TODO it is easier if we create this before hand. essentially a list of what features we care about
    #ie fname, lname, etc. Should model our standardized data. they should each be a dict themselves, 
    #so that we can associate a value with them
    unique_features = {}

    for query in queries: #loop through each endpoints query
        
        #TODO calculate the unique time factor for each edpoint depending on 
        #how recently it was updated. will be something like last updated scaled by our time_factor
        unique_tf = 1

        if query != None: #some endpoints might not have the person

            #should match unique features
            for index, (key, value) in enumerate(query.items()): #TODO figure out how looping through each feature of an input will work in regards to our container

                if key not in unique_features: #add each unique feature to our dict
                    unique_features[key] = {}

                if value in unique_features[key]:
                    unique_features[key][value] += (1 * unique_tf) #might not update, if so try .get()

                else: 
                    unique_features[key][value] = (1 * unique_tf)#needs testing, but I think this adds a new feature val with a vote
    
    highest_features = [] #dict of the highest voted result for each feature
    highest_features = {feature: max(options, key=options.get) for feature, options in unique_features.items()}


    print(highest_features)

    return highest_features


if __name__ == "__main__":
    predict(test_data, 0)
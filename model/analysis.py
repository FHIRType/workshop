#Author: Iain Richey
####################
#This file ccontains the different analysis models for the different types of queries
#if you are lookin for the test of the models, they are in the other file
####################

test_prac = [
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 37},
    {'fname': 'Johnny', 'lname': 'Weaver', 'npi': '123456', 'age': 22, 'gender': 'Male'},
    {'fname': 'Iain', 'lname': 'Richey', 'npi': '137681', 'age': 37},
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 40}
]

test_prac_role = [
    {'id': 1578, 'active': True, 'identifier': '1'},
    {'id': 1578, 'active': True, 'identifier': '1'},
    {'id': 1578, 'active': False, 'identifier': '2'},
    {'id': 1578, 'active': False, 'identifier': '1'}
]

test_location = [
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'Jerry bone emporium'},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'whitebird'},
    {'id': 129, 'status': 'active', 'phone': "581-234-9872", 'address': '872 real ave', 'name': 'Jerry bone emporium'},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '993 not real lane', 'name':'Jerry bone emporium'}
]

####################
#This function takes in a set of queries to the various endpoints, and analyses them for the
# most likely results 
####################
def predict(queries, time_factor) -> dict: #will return whatever our container class is 
    unique_features = {}

    for query in queries: #loop through each endpoints query
        
        #TODO calculate the unique time factor for each edpoint depending on 
        #how recently it was updated. will be something like last updated scaled by our time_factor
        unique_tf = 1

        if query != None: #some endpoints might not have the person

            #should match unique features
            for index, (key, value) in enumerate(query.items()):

                if key not in unique_features: #add each unique feature to our dict
                    unique_features[key] = {}

                if value in unique_features[key]:
                    unique_features[key][value] += (1 * unique_tf)

                else: 
                    unique_features[key][value] = (1 * unique_tf)

    for key in unique_features:
        print(unique_features[key])
    
    highest_features = [] #dict of the highest voted result for each feature
    highest_features = {feature: max(options, key=options.get) for feature, options in unique_features.items()}


    print(highest_features)

    return highest_features


if __name__ == "__main__":
    predict(test_prac, 0)
    print("\n")
    predict(test_prac_role, 0)
    print("\n")
    predict(test_location, 0)
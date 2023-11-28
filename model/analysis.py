#Author: Iain Richey
####################
#This file ccontains the different analysis models for the different types of queries
#if you are lookin for the test of the models, they are in the other file
####################
from datetime import datetime, timedelta

test_prac = [
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 37, 'last_updated': ''},
    {'fname': 'Johnny', 'lname': 'Weaver', 'npi': '123456', 'age': 22, 'gender': 'Male', 'last_updated': ''},
    {'fname': 'Iain', 'lname': 'Richey', 'npi': '137681', 'age': 37, 'last_updated': ''},
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 40, 'last_updated': ''}
]

test_prac_role = [
    {'id': 1578, 'active': True, 'identifier': '1', 'last_updated': ''},
    {'id': 1578, 'active': True, 'identifier': '1', 'last_updated': ''},
    {'id': 1578, 'active': False, 'identifier': '2', 'last_updated': ''},
    {'id': 1578, 'active': False, 'identifier': '1', 'last_updated': ''}
]

test_location = [
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'Jerry bone emporium', 'last_updated': ''},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'whitebird', 'last_updated': ''},
    {'id': 129, 'status': 'active', 'phone': "581-234-9872", 'address': '872 real ave', 'name': 'Jerry bone emporium', 'last_updated': ''},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '993 not real lane', 'name':'Jerry bone emporium'}
]

####################
#This function takes in a set of queries to the various endpoints, and analyses them for the
# most likely results 
####################
def predict(queries, time_factor) -> dict: #will return whatever our container class is 
    unique_features = {}
    today = datetime.today()

    for query in queries: #loop through each endpoints query
        
        #TODO calculate the unique time factor for each edpoint depending on 
        #how recently it was updated. will be something like last updated scaled by our time_factor

        last_updated = query["last_updated"]
        time_diff = today - last_updated.date()
        del query["last_updated"] #get it outta there

        #the scale that we are going to apply to our vote
        unique_tf = 1 - (1 * (time_factor * time_diff))

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
    # predict(test_prac, 0)
    # print("\n")
    # predict(test_prac_role, 0)
    # print("\n")
    # predict(test_location, 0)

    time1 = datetime.fromisoformat("2022-11-15T23:05:21-08:00")
    time2 = datetime.fromisoformat("2023-05-16T10:30:00+05:00")

    print(time1.date())

    print(time2.date())

    print(time1.date() - time2.date())

    print(datetime.today())

    today = datetime.today()

    diff1 = (today.date() - time1.date())

    diff2 = (today.date() - time2.date())

    print("time 1 is different from today by ", diff1.days)

    print("time 2 is different from today by ", diff2.days)
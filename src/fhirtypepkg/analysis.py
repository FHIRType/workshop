#Author: Iain Richey
####################
#This file ccontains the different analysis models for the different types of queries
#if you are lookin for the test of the models, they are in the other file
####################
from datetime import datetime, timedelta
from fhirtypepkg.standardize import KEY_TIME

test_prac = [
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 37, 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'fname': 'Johnny', 'lname': 'Weaver', 'npi': '123456', 'age': 22, 'gender': 'Male', 'last_updated': '2022-11-15T23:05:21-08:00'},
    {'fname': 'Iain', 'lname': 'Richey', 'npi': '137681', 'age': 37, 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'fname': 'John', 'lname': 'Weaver', 'npi': '123456', 'age': 40, 'last_updated': '2022-11-15T23:05:21-08:00'}
]

test_prac_role = [
    {'id': 1578, 'active': True, 'identifier': '1', 'last_updated': '2022-11-15T23:05:21-08:00'},
    {'id': 1578, 'active': True, 'identifier': '1', 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'id': 1578, 'active': False, 'identifier': '2', 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'id': 1578, 'active': False, 'identifier': '1', 'last_updated': '2022-11-15T23:05:21-08:00'}
]

test_location = [
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'Jerry bone emporium', 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '1234 fake street', 'name': 'whitebird', 'last_updated': '2022-11-15T23:05:21-08:00'},
    {'id': 129, 'status': 'active', 'phone': "581-234-9872", 'address': '872 real ave', 'name': 'Jerry bone emporium', 'last_updated': '2023-05-16T10:30:00+05:00'},
    {'id': 137, 'status': 'active', 'phone': "581-234-9872", 'address': '993 not real lane', 'name':'Jerry bone emporium', 'last_updated': '2022-11-15T23:05:21-08:00'}
]

####################
#This function takes in a set of queries to the various endpoints, and analyses them for the
# most likely results 
####################
def predict(queries, time_factor) -> dict: #will return whatever our container class is 
    unique_features = {}
    today = datetime.today()

    for query in queries: #loop through each endpoints query

        last_updated = datetime.fromisoformat(query[KEY_TIME])

        time_diff = (today.date() - last_updated.date()) #currently it splits into weeks
        time_diff = time_diff.days // 7

        print("last_updated is ", last_updated, "time diff is ", time_diff)

        #the scale that we are going to apply to our vote. as time_diff grows, our unique time factor gets smnaller
        unique_tf = (1 * (time_factor * time_diff))

        print("unique_tf is ", unique_tf)

        if query != None: #some endpoints might not have the person

            #matches unique features (ie no repeats)
            for index, (key, value) in enumerate(query.items()):

                if key not in unique_features: #add each unique feature to our dict
                    unique_features[key] = {}

                if value in unique_features[key]:
                    unique_features[key][value] += unique_tf

                else: 
                    unique_features[key][value] = unique_tf

    for key in unique_features:
        print(unique_features[key])
    
    highest_features = [] #dict of the highest voted result for each feature
    highest_features = {feature: max(options, key=options.get) for feature, options in unique_features.items() if feature != "last_updated"}


    print(highest_features)

    return highest_features

#TODO 1: if something is updated too long ago it actually gets extra votes, cuz 0.001 * 1000 weeks becomes 10 for ex
#2: needs testing for good hyper params, and possibly better equation to find unique_tf.
#3: should also decide if by week is good, or would rather do by day or something else

if __name__ == "__main__":
    predict(test_prac, 0.01)
    print("\n")
    # predict(test_prac_role, 0)
    # print("\n")
    # predict(test_location, 0)

    # time1 = datetime.fromisoformat("2022-11-15T23:05:21-08:00")
    # time2 = datetime.fromisoformat("2023-05-16T10:30:00+05:00") 

    # print(time1.date())

    # print(time2.date())

    # print(time1.date() - time2.date())

    # print(datetime.today())

    # today = datetime.today()

    # diff1 = (today.date() - time1.date())

    # diff2 = (today.date() - time2.date())

    # print("time 1 is different from today by ", diff1.days // 7)

    # print("time 2 is different from today by ", diff2.days // 7)
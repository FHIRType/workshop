#Author: Iain Richey


####################
#This file ccontains the different analysis models for the different types of queries
#if you are lookin for the test of the models, they are in the other file
####################



####################
#This function takes in a set of queries to the various endpoints, and analyses them for the
# most likely results 
#
####################
def predict_practitioner(queries, time_factor) -> query: #will return whatever our container class is 
    #TODO change up params and setup depending on if the endpoints are 
    #quieried before this step, or during it 

    #TODO it is easier if we create this before hand. essentially a list of what features we care about
    #ie fname, lname, etc. Should model our standardized data. they should each be a dict themselves, 
    #so that we can associate a value with them
    unique_features = []

    for query in queries: #loop through each endpoints query
        
        #TODO calculate the unique time factor for each edpoint depending on 
        #how recently it was updated 
        unique_tf

        if query != None: #some endpoints might not have the person

            #should match unique features
            for index, value in enumerate(query): #TODO figure out how looping through each feature of an input will work in regards to our container

                if value not in unique_features[index]: #needs testing, but I think this adds a new feature val with a vote
                    unique_features[index][value] = (1 * unique_ft)

                else: #TODO clean this up, not totally sure if it works. trying to deal with dicts can be weird
                    unique_features[index][value] += (1 * unique_ft) #might not update, if so try .get()
    
    #TODO implement testing, for the first test just give it one simple one without calcing unique_tf, and see if it corretly
    #calculates each unique value for each feature and the votes for it. 


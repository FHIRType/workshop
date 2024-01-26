from flask_restx import Resource, Namespace

ns = Namespace("api")


# api/getdata
# Description: Given a first name, last name, and NPI
# the routes retrieve data from all endpoints or specified endpoints.
# return data as JSON, a file, or web page.
# Optionally it could contain an attribute to limit or
# specify the endpoints used to gather data.
# It should use an object to serialize and de-serialize the flattened data.
@ns.route("/getdata")
class GetData(Resource):
    def get(self):
        return {"the": "data"}


# Given a list of JSON of flattened data,
# the service should attempt to match records
# and return all records as list of lists.
@ns.route("/matchdata")
class MatchData(Resource):
    def get(self):
        return {"match": "data"}


# Given a group of matched records,
# return those records with a consensus result
# and an accuracy score built in.
@ns.route("/consensusresult")
class ConsensusResult(Resource):
    def post(self):
        return { "consensus": "result"}
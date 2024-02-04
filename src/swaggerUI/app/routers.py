from flask_restx import Resource, Namespace, reqparse, abort
from .extensions import api
from .models import practitioner
from fhirtypepkg.main import search_practitioner

ns = Namespace("api")
parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='The first name of the practitioner')
parser.add_argument('last_name', type=str, help='The last name of the practitioner')
parser.add_argument('npi', type=str, help='The NPI of the practitioner')
parser.add_argument('endpoint', type=str, help='The type of the endpoint')

# api/getdata
# Description: Given a first name, last name, and NPI
# the routes retrieve data from all endpoints or specified endpoints.
# return data as JSON, a file, or web page.
# Optionally it could contain an attribute to limit or
# specify the endpoints used to gather data.
# It should use an object to serialize and de-serialize the flattened data.
@ns.route("/getdata")
class GetData(Resource):
    @ns.doc('Retrieve data from all endpoints or specified endpoints')
    @ns.expect(parser)
    @ns.marshal_list_with(practitioner)
    def get(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        npi = args['npi']

        if first_name and last_name and npi:
            return search_practitioner(first_name, last_name, npi)[2]
        else:
            abort(400, message="All required queries must be provided")

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
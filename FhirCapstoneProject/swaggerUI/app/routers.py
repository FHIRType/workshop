from flask_restx import Resource, Namespace, reqparse, abort
from flask import make_response, Flask, render_template, send_file, jsonify
import json

from .extensions import api, search_practitioner
from io import BytesIO
from .models import practitioner

test_data = {
    "Endpoint": "testEndpoint",
    "DateRetrieved": "01-21-2024",
    "FullName": "John Smith",
    "NPI": "0112031311",
    "FirstName": "John",
    "LastName": "Smith",
    "Gender": "Male",
    "Taxonomy": "X02332D2",
    "GroupName": "Orthodontist",
    "ADD1": "1234 SW Ave",
    "ADD2": "5678 NW Ave",
    "City": "Chicago",
    "State": "Illinois",
    "Zip": "12234",
    "Phone": "9712131234",
    "Fax": "5031231234",
    "Email": "abc@gmail.com",
    "lat": "lat_data",
    "lng": "lng_data",
    "LastPracUpdate": "LastPracUpdate_data",
    "LastPracRoleUpdate": "LastPracRoleUpdate_data",
    "LastLocationUpdate": "LastLocationUpdate_data",
    "AccuracyScore": "acc_score_data"
},

ns = Namespace("api")
parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='The first name of the practitioner')
parser.add_argument('last_name', type=str, help='The last name of the practitioner')
parser.add_argument('npi', type=str, help='The NPI of the practitioner')
parser.add_argument('endpoint', type=str, help='The type of the endpoint')
parser.add_argument('format', type=str, help='The type of the returned data')

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
    #@ns.marshal_list_with(practitioner)
    def get(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        npi = args['npi']
        format = args['format']

        all_results, flatten_data = search_practitioner(
            first_name, last_name, npi
        )
        print(all_results)
        pretty_printed_json = json.dumps(flatten_data, indent=4)
        print(pretty_printed_json)

        if first_name and last_name and npi:
            if format == "page":
                return make_response(render_template('app.html', json_data=test_data))
            elif format == "file":
                json_data = test_data
                json_str = json.dumps(json_data, indent=4)
                file_bytes = BytesIO()
                file_bytes.write(json_str.encode('utf-8'))
                file_bytes.seek(0)
                return send_file(file_bytes, as_attachment=True, attachment_filename="test_file.json")
            else:
                return test_data

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
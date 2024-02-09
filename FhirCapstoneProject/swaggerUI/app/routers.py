from flask_restx import Resource, Namespace, reqparse, abort
from flask import make_response, Flask, render_template, send_file, jsonify
import json
from .extensions import api
from io import BytesIO
from .models import practitioner, error
from FhirCapstoneProject.fhirtypepkg.main import search_practitioner
from .data import api_description

test_data = (
    {
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
        "AccuracyScore": 85,
    },
)

ns = Namespace("api", description='API endpoints related to Practitioner.')
parser = reqparse.RequestParser()
parser.add_argument("first_name", required=True, type=str, help="The first name of the practitioner")
parser.add_argument("last_name", required=True, type=str, help="The last name of the practitioner")
parser.add_argument("npi", required=True, type=str, help="The NPI of the practitioner")
parser.add_argument("endpoint", action='split', type=str, help="The type of the endpoint (default: All)")
parser.add_argument("format", type=str, choices=('file', 'page'), help="The type of the returned data - returns JSON format by default.")


# api/getdata
@ns.route("/getdata")
class GetData(Resource):
    @ns.expect(parser)
    @ns.response(200, 'The data was successfully retrieved.', practitioner)
    @ns.response(400, 'Invalid request. Check the required queries.', error)
    @ns.response(404, 'Could not find the practitioner with given data.', error)
    @ns.doc(description=api_description["getdata"])
    @ns.marshal_list_with(practitioner)
    def get(self):
        args = parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        npi = args["npi"]
        return_type = args["format"]

        # TODO: Call actual function later
        # print(search_practitioner(first_name, last_name, npi)[1])

        if first_name and last_name and npi:
            if return_type == "page":
                return make_response(render_template("app.html", json_data=test_data))
            elif return_type == "file":
                json_data = test_data
                json_str = json.dumps(json_data, indent=4)
                file_bytes = BytesIO()
                file_bytes.write(json_str.encode("utf-8"))
                file_bytes.seek(0)
                return send_file(
                    file_bytes, as_attachment=True, attachment_filename="test_file.json"
                )
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
        return {"consensus": "result"}

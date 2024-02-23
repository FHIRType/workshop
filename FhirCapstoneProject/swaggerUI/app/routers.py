from .models import practitioner, error
from .data import api_description
from flask_restx import Resource, Namespace, reqparse, abort
from flask import make_response, Flask, render_template, send_file, jsonify
import json
from .extensions import api, search_practitioner, print_resource
from .parsers import get_data_parser
from io import BytesIO
from .models import practitioner
from .utils import validate_inputs

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
    "AccuracyScore": "85",
}


ns = Namespace("api", description="API endpoints related to Practitioner.")

# api/getdata
@ns.route("/getdata")
class GetData(Resource):
    @ns.expect(get_data_parser)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.doc(description=api_description["getdata"])
    def get(self):
        args = get_data_parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        npi = args["npi"]
        return_type = args["format"]

        practitioner_all_results, flatten_practitioner_data = search_practitioner(last_name, first_name, npi)
        # role_all_results, fatten_role_data = search_practitioner_role(last_name, first_name, npi)

        # Validate the user's queries
        # If they are invalid, throw status code 400 with an error message
        validation_result = validate_inputs(test_data)
        if not validation_result["success"]:
            # abort(validation_result["status_code"], message=validate_inputs(test_data)["message"])
            abort(
                validation_result["status_code"],
                message=validate_inputs(flatten_practitioner_data)["message"],
            )

        if first_name and last_name and npi:
            if return_type == "page":
                # return make_response(render_template("app.html", json_data=test_data))
                return make_response(
                    render_template("app.html", json_data=flatten_practitioner_data)
                )
            elif return_type == "file":
                json_data = flatten_data
                # json_data = test_data
                json_str = json.dumps(json_data, indent=4)
                file_bytes = BytesIO()
                file_bytes.write(json_str.encode("utf-8"))
                file_bytes.seek(0)
                return send_file(
                    file_bytes, as_attachment=True, download_name="getdata.json"
                )
            else:
                return flatten_practitioner_data
                # return test_data

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

from .models import practitioner, error
from .data import api_description
from flask_restx import Resource, Namespace, reqparse, abort
from flask import make_response, Flask, render_template, send_file, jsonify
import json
from .extensions import api, search_practitioner, search_practitioner_role, search_location, search_all_practitioner_data, print_resource
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
parser = reqparse.RequestParser()
parser.add_argument(
    "first_name", required=True, type=str, help="The first name of the practitioner"
)
parser.add_argument(
    "last_name", required=True, type=str, help="The last name of the practitioner"
)
parser.add_argument("npi", required=True, type=str, help="The NPI of the practitioner")
parser.add_argument(
    "endpoint", action="split", type=str, help="The type of the endpoint (default: All)"
)
parser.add_argument(
    "format",
    type=str,
    choices=("file", "page"),
    help="The type of the returned data - returns JSON format by default.",
)


# api/getdata
@ns.route("/getdata")
class GetData(Resource):
    @ns.expect(parser)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.doc(description=api_description["getdata"])
    def get(self):
        args = parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        npi = args["npi"]
        return_type = args["format"]

        # TODO: Call actual function later
        # all_results, flatten_data = search_practitioner("Dykstra", "Michelle", "1013072586")
        all_results, flatten_data = search_all_practitioner_data("Dykstra", "Michelle", "1013072586")
        print_resource(all_results)
        # print(all_results)
        # pretty_printed_json = json.dumps(flatten_data, indent=4)
        # print(pretty_printed_json)

        # Validate the user's queries
        # If they are invalid, throw status code 400 with an error message
        validation_result = validate_inputs(test_data)
        if not validation_result["success"]:
            # abort(validation_result["status_code"], message=validate_inputs(test_data)["message"])
            abort(
                validation_result["status_code"],
                message=validate_inputs(flatten_data)["message"],
            )

        if first_name and last_name and npi:
            if flatten_data is None:
                abort(404, "Didn't find anyone!")
            else:
                if return_type == "page":
                    # return make_response(render_template("app.html", json_data=test_data))
                    return make_response(
                        render_template("app.html", json_data=flatten_data)
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
                    return flatten_data
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

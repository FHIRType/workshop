import json
from io import BytesIO

import asyncio
from dotenv import load_dotenv
from flask import make_response, render_template, send_file, request
from flask_restx import Resource, Namespace, abort

from .data import api_description
from .extensions import (
    search_all_practitioner_data,
    match_data,
    predict,
    calc_accuracy,
    gather_all_data,
)
from .models import error, practitioners_list_model, consensus_fields
from .models import practitioner
from .parsers import get_data_parser, get_list_data_parser
from .utils import validate_inputs, validate_npi

load_dotenv()

ns = Namespace("api", description="API endpoints related to Practitioner.")


# api/getdata
@ns.route("/getdata")
class GetData(Resource):
    @ns.expect(get_data_parser)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.response(429, "Too Many Requests response", error)
    @ns.response(500, "Internal server error.", error)
    @ns.doc(description=api_description["getdata"])
    def get(self):
        args = get_data_parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        npi = args["npi"]
        endpoint = args["endpoint"]
        return_type = args["format"]

        flatten_data = asyncio.run(
            search_all_practitioner_data(last_name, first_name, npi, endpoint)
        )

        # Validate the user's queries
        # If they are invalid, throw status code 400 with an error message
        if first_name and last_name and npi:
            if flatten_data is None or len(flatten_data) < 1:
                abort_message = (
                    "Could not find practitioner with name "
                    + first_name
                    + " "
                    + last_name
                    + " and npi: "
                    + npi
                )
                abort(404, abort_message)
            else:
                for data in flatten_data:
                    validation_result = validate_inputs(data)
                    if not validation_result["success"]:
                        abort(
                            validation_result["status_code"],
                            message=validate_inputs(data)["message"],
                        )
                if return_type == "page":
                    return make_response(
                        render_template("app.html", json_data=flatten_data)
                    )
                elif return_type == "file":
                    json_data = flatten_data
                    json_str = json.dumps(json_data, indent=4)
                    file_bytes = BytesIO()
                    file_bytes.write(json_str.encode("utf-8"))
                    file_bytes.seek(0)
                    return send_file(
                        file_bytes, as_attachment=True, download_name="getdata.json"
                    )
                else:
                    return flatten_data

        else:
            abort(400, message="All required queries must be provided")

    @ns.expect(practitioners_list_model, get_list_data_parser)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.response(429, "Too Many Requests response", error)
    @ns.response(500, "Internal server error.", error)
    @ns.doc(description=api_description["getlistdata"])
    def post(self):
        args = get_list_data_parser.parse_args()
        endpoints = args["endpoint"] if args["endpoint"] != 'All' else None
        return_type = args["format"]
        consensus = True if args["consensus"][0] == "T" else False

        request_body = request.json
        data_list = request_body["practitioners"]
        res = {
            "message": "No practitioners were found"
        }

        tasks = []
        for data in data_list:
            if validate_npi(data['npi']):
                npi = data["npi"]
                first_name = data["first_name"]
                last_name = data["last_name"]
                tasks.append(
                    search_all_practitioner_data(last_name, first_name, npi, endpoint=endpoints, consensus=consensus)
                )
            else:
                abort(400, message="Invalid NPI: NPI should be 10 digit number")

        all_responses = asyncio.run(gather_all_data(tasks))

        if all_responses[0] is not None:
            res = {}
            for response in all_responses:
                if response:
                    for data in response:
                        if data["NPI"] in res.keys():
                            res[data["NPI"]].append(data)
                        else:
                            res[data["NPI"]] = [data]

        # Processing the output format
        if return_type == "File":
            json_data = res
            json_str = json.dumps(json_data, indent=4)
            file_bytes = BytesIO()
            file_bytes.write(json_str.encode("utf-8"))
            file_bytes.seek(0)
            return send_file(
                file_bytes, as_attachment=True, download_name="getdata.json"
            )
        elif return_type == "Page":
            return make_response(render_template("list.html", json_data=res))
        else:
            return res


@ns.route("/matchdata")
@ns.response(200, "The data was successfully retrieved.", practitioner)
@ns.response(400, "Invalid request. Check the required fields.", error)
@ns.response(404, "Could not find the practitioner with given data.", error)
@ns.response(429, "Too Many Requests response", error)
@ns.response(500, "Internal server error.", error)
@ns.doc(description=api_description["matchdata"])
class MatchData(Resource):
    @ns.expect(consensus_fields)
    def post(self):
        # Extracting the JSON data from the incoming request
        user_data = request.json["collection"]
        use_tax = request.json.get("use_taxonomy", False)

        # Pass the user data to your processing function
        response = match_data(user_data, use_tax)

        for list in response:
            if len(list) != 1:
                concencus = predict(list)
                list = calc_accuracy(list, concencus)
                list.append(concencus)

        return response


# Given a group of matched records,
# return those records with a consensus result
# and an accuracy score built in.
@ns.route("/getconsensus")
class ConsensusResult(Resource):
    @ns.expect(get_data_parser)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.response(429, "Too Many Requests response", error)
    @ns.response(500, "Internal server error.", error)
    @ns.doc(description=api_description["getconsensus"])
    def get(self):
        args = get_data_parser.parse_args()
        first_name = args["first_name"]
        last_name = args["last_name"]
        npi = args["npi"]
        return_type = args["format"]

        flatten_data = asyncio.run(
            search_all_practitioner_data(last_name, first_name, npi, consensus=True)
        )

        # Validate the user's queries
        # If they are invalid, throw status code 400 with an error message
        if first_name and last_name and npi:
            if flatten_data is None or len(flatten_data) < 1:
                abort_message = (
                    "Could not find practitioner with name "
                    + first_name
                    + " "
                    + last_name
                    + " and npi: "
                    + npi
                )
                abort(404, abort_message)
            else:
                for data in flatten_data:
                    validation_result = validate_inputs(data)
                    if not validation_result["success"]:
                        abort(
                            validation_result["status_code"],
                            message=validate_inputs(data)["message"],
                        )
                if return_type == "page":
                    return make_response(
                        render_template("app.html", json_data=flatten_data)
                    )
                elif return_type == "file":
                    json_data = flatten_data
                    json_str = json.dumps(json_data, indent=4)
                    file_bytes = BytesIO()
                    file_bytes.write(json_str.encode("utf-8"))
                    file_bytes.seek(0)
                    return send_file(
                        file_bytes, as_attachment=True, download_name="getdata.json"
                    )
                else:
                    return flatten_data

        else:
            abort(400, message="All required queries must be provided")

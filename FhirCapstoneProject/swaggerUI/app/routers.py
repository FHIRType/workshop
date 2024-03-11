from .models import error
from .data import api_description
from flask_restx import Resource, Namespace, reqparse, abort, fields
from flask import make_response, Flask, render_template, send_file, jsonify, request

import os
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_openai import OpenAI, ChatOpenAI
from langchain_experimental.agents import create_csv_agent

import json
from .extensions import (
    api,
    search_all_practitioner_data,
)
from .parsers import get_data_parser, get_question_parser
from io import BytesIO
from .models import practitioner
from .utils import validate_inputs, validate_npi

load_dotenv()

ns = Namespace("api", description="API endpoints related to Practitioner.")

name_fields = api.model('Name', {
    "first_name": fields.String,
    "last_name": fields.String
})

npi_fields = api.model('NPI', {
    "npi": fields.Nested(name_fields)
})

list_fields = api.model('ListData', {
    "data": fields.List(fields.Nested(npi_fields)),
    "format": fields.String
})


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

        flatten_data = search_all_practitioner_data(last_name, first_name, npi)

        # Validate the user's queries
        # If they are invalid, throw status code 400 with an error message
        if first_name and last_name and npi:
            if flatten_data is None or len(flatten_data) < 1:
                abort_message = "Could not find practitioner with name " + first_name + " " + last_name + " and npi: " + npi
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

    @ns.expect(list_fields)
    @ns.response(200, "The data was successfully retrieved.", practitioner)
    @ns.response(400, "Invalid request. Check the required queries.", error)
    @ns.response(404, "Could not find the practitioner with given data.", error)
    @ns.doc(description=api_description["getlistdata"])
    def post(self):
        request_body = request.json
        data_list = request_body["data"]
        return_type = "default"
        if "format" in request_body.keys():
            return_type = request_body["format"]
        res = {}

        for data in data_list:
            for key, value in data.items():
                if validate_npi(key):
                    npi = key
                    first_name = value["first_name"]
                    last_name = value["last_name"]
                    flatten_data = search_all_practitioner_data(last_name, first_name, npi)
                    res[npi] = flatten_data
                else:
                    abort(400, message="Invalid NPI: NPI should be 10 digit number")

        # Processing the output format
        if return_type == "file":
            json_data = res
            json_str = json.dumps(json_data, indent=4)
            file_bytes = BytesIO()
            file_bytes.write(json_str.encode("utf-8"))
            file_bytes.seek(0)
            return send_file(file_bytes, as_attachment=True, download_name="getdata.json")
        elif return_type == "page":
            return make_response(
                render_template("list.html", json_data=res)
            )
        else:
            return res
        return res


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
    def get(self):
        return {"consensus": "result"}


@ns.route("/askai")
class GetLangChainAnswer(Resource):
    @ns.expect(get_question_parser)
    def get(self):
        args = get_question_parser.parse_args()
        question = args["question"]
        prompt = f"Answer strictly from the dataset provided: {question}"
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-4", api_key=os.getenv("OPENAI_API_KEY")),
            "./FhirCapstoneProject/swaggerUI/app/bulk_provider_data.csv",
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS
            # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )
        response = agent.invoke({"input": prompt})
        print(response)

        return {"answer": response['output']}

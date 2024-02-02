from flask import Flask, render_template, send_file, jsonify, request
import json
import os
from io import BytesIO

app = Flask(__name__)


"""
Example data that is a list of dictionaries with different attributes
"""

# Test data
test_data = [{
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
{
    "Endpoint": "testEndpoint2",
    "DateRetrieved": "02-01-2024",
    "FullName": "Jeff Johnson",
    "NPI": "0131221",
    "FirstName": "Jeff",
    "LastName": "Johnson",
    "Gender": "Male",
    "Taxonomy": "X012311",
    "GroupName": "Physician",
    "ADD1": "1311 SW Ave",
    "ADD2": "4311 NW Ave",
    "City": "Austin",
    "State": "Texas",
    "Zip": "12234",
    "Phone": "5031311311",
    "Fax": "5031233234",
    "Email": "jeffbezos@gmail.com",
    "lat": "lat_data",
    "lng": "lng_data",
    "LastPracUpdate": "LastPracUpdate_data",
    "LastPracRoleUpdate": "LastPracRoleUpdate_data",
    "LastLocationUpdate": "LastLocationUpdate_data",
    "AccuracyScore": "acc_score_data"
},
{
    "Endpoint": "testEndpoint3",
    "DateRetrieved": "02-02-2024",
    "FullName": "Alice Johnson",
    "NPI": "0213456",
    "FirstName": "Alice",
    "LastName": "Johnson",
    "Gender": "Female",
    "Taxonomy": "X045678",
    "GroupName": "Pediatrician",
    "ADD1": "789 Elm St",
    "ADD2": "Apt 202",
    "City": "Los Angeles",
    "State": "California",
    "Zip": "90001",
    "Phone": "2135557890",
    "Fax": "2135551234",
    "Email": "alice.johnson@example.com",
    "lat": "lat_data",
    "lng": "lng_data",
    "LastPracUpdate": "LastPracUpdate_data",
    "LastPracRoleUpdate": "LastPracRoleUpdate_data",
    "LastLocationUpdate": "LastLocationUpdate_data",
    "AccuracyScore": "acc_score_data"
}]

# @app.route("/", methods=["GET"])
# def get_data():
#     """
#     Given a list of flattened FHIR data this endpoint will render a table for json object
#     """
#
#     return render_template("app.html", json_data=test_data)


@app.route("/", methods=["GET", "POST"])  # Controller: what Flask Controls
def index():  # Model
    """
    Given a list of flattened FHIR data this endpoint will use POST method
    in order to display the data to the user
    In order to render that data, we will redirect it to the html file
    """
    if request.method == "GET":
        return render_template("app.html", json_data=test_data)
    elif request.method == "POST":
        request_json = request.json
        # View: coding view as app.html with Model data being passed
        return render_template("app.html", json_data=request_json)

@app.route("/data", methods=["GET", "POST"])
def get_data():
    """
    Endpoint to retrieve data based on key-value pairs passed via GET or POST method
    """
    if request.method == "GET":
        endpoint = request.args.get('Endpoint')
        data = next((entry for entry in test_data if entry["Endpoint"] == endpoint), None)
        if data:
            return jsonify(data)
            # return render_template("app.html", json_data=jsonify(data))
        else:
            return jsonify({"error": f"Data not found for endpoint: {endpoint}"}), 404

    elif request.method == "POST":
        request_data = request.json
        response_data = []

        for item in request_data:
            endpoint = item.get('Endpoint')
            data = next((entry for entry in test_data if entry["Endpoint"] == endpoint), None)

            if data:
                response_data.append(data)
            else:
                response_data.append({"error": f"Data not found for endpoint: {endpoint}"})

        return jsonify(response_data)
        # return render_template("app.html", json_data=jsonify(response_data))

# Method probably needs to be a GET method,
# we want someone to navigate to it and download the file
# A POST would get more data secured than a GET method
@app.route("/download", methods=["GET", "POST"])
def download_file():
    """

    We want to make a file that lives in memory since some servers in
    file path doesn't have enough disk space

    This will accept a json string and converts into list of dictionaries
    and write to file:

    - Converts dictionary to a string in bytes
    - Make byte object
    - Fill utf-8 encoded string as bytes into bytes object
    - Place bytes into a file

    """

    if request.method == "GET":
        json_data = test_data
        json_str = json.dumps(json_data, indent=4)
        file_bytes = BytesIO()
        file_bytes.write(json_str.encode('utf-8'))
        file_bytes.seek(0)
        return send_file(file_bytes, as_attachment=True, attachment_filename="testfile.json")
    elif request.method == "POST":
        # test_data = request.json
        req_json = request.json
        # json_data = json.dumps(test_data, indent=4)
        json_data = json.dumps(req_json, indent=4)
        file_bytes = BytesIO()
        file_bytes.write(json_data.encode('utf-8'))
        file_bytes.seek(0)
        # Make it redirect
        return send_file(file_bytes, as_attachment=True, attachment_filename="testfile.json")


# TODO: Provide a GET endpoint for each endpoint
# From POST redirect to a GET and pass in the data
# using GET req.args


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3045)
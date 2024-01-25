from flask import Flask, render_template, send_file, jsonify
import json

# import fhirtypepkg
# from fhirtypepkg.client import SmartClient

app = Flask(__name__)

# Create an instance of SmartClient class
# smart_client = SmartClient()


"""
Example data
"""

data = {
    "Endpoint": "kpx-service-bus.kp.org/service/hp/mhpo/healthplanproviderv1rc/",
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
}

# Serialize the data to a JSON-formatted string
serialized_data = json.dumps(data, indent=2)
print("Serialized Data:")
print(serialized_data)

# Deserialize the JSON-formatted string back to a Python object
deserialized_data = json.loads(serialized_data)
print("\nDeserialized Data:")
print(deserialized_data)


@app.route("/")
def index():
    """
    TODO:
    - Call endpoints from SmartClient?
    - render the html with the data objects and display it

    :return:
    """

    json_data = json.dumps(data, indent=2)
    return render_template("public/app.html", json_data=json_data)


"""
TODO:
Download list of object to a file by:
- Calling a function that creates the file
- Serve the file for download
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3045)
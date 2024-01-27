from flask import Flask, render_template, send_file, jsonify
import json
import os

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


"""TODO:"""
## FirstName
## for list in objects that contains attribute object.firstname
##displays all firstname in a table

##Feed in json object through post
##or be able to accept an object from model and display it

##model view controller


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
Download list of object to a file by:
- Calling a function that creates the file
- Serve the file for download
"""



@app.route("/download", methods=["GET"])
def download_file():

    # Create a temp JSON file
    # Give it a specific path
    temp_file_path = f"data_files/temp_data.json"
    with open(temp_file_path, "w") as f:
        json.dump(data, f, indent=2)

    # Serve the file for download
    return send_file(temp_file_path, as_attachment=True)


# Unit test for checking if data matches in the downloaded file

def test_download_same_data():
    # Simulate a request to the download endpoint
    response = app.test_client().get('/download')

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the Content-Disposition header is set to attachment
    assert 'attachment' in response.headers['Content-Disposition']

    # Save the downloaded file content
    with open("downloaded_data.json", "wb") as f:
        f.write(response.data)

    # Read the content of the downloaded file
    with open("downloaded_data.json", "r") as f:
        downloaded_data = json.load(f)

    # Check if the downloaded data matches the original data
    assert downloaded_data == data

    # Clean up the temporary file
    os.remove("downloaded_data.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3045)
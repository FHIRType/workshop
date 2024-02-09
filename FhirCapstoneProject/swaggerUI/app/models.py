from flask_restx import fields
from .extensions import api

practitioner = api.model(
    "Practitioner",
    {
        "Endpoint": fields.String(
            readonly=True, description="The source endpoint of the information"
        ),
        "DateRetrieved": fields.String(readonly=True, description="The retrieved date"),
        "FullName": fields.String(readonly=True, description="The full name of the practitioner"),
        "NPI": fields.String(readonly=True, description="NPI of the practitioner"),
        "FirstName": fields.String(readonly=True, description="The first name of the practitioner"),
        "LastName": fields.String(readonly=True, description="The last name of the practitioner"),
        "Gender": fields.String(readonly="The gender of the practitioner"),
        "Taxonomy": fields.String(readonly=True, description="The practitioner's taxonomy"),
        "GroupName": fields.String(readonly=True, description="The group name data of the practitioner"),
        "ADD1": fields.String(readonly=True, description="The first address"),
        "ADD2": fields.String(readonly=True, description="The second address"),
        "City": fields.String(readonly=True, description="The city"),
        "State": fields.String(readonly=True, description="The state"),
        "Zip": fields.String(readonly=True, description="The ZIP code"),
        "Phone": fields.String(readonly=True, description="The phone number of the practitioner"),
        "Fax": fields.String(readonly=True, description="The fax number of the practitioner"),
        "Email": fields.String(readonly=True, description="The email address of the practitioner"),
        "lat": fields.String(readonly=True, description="The latitude"),
        "lng": fields.String(readonly=True, description="The longitude"),
        "LastPracUpdate": fields.String(readonly=True, description="The last updated date of the Practitioner information"),
        "LastPracRoleUpdate": fields.String(
            readonly=True, description="The last updated date of the Practitioner Role information"
        ),
        "LastLocationUpdate": fields.String(
            readonly=True, description="The last updated date of the Location information"
        ),
        "AccuracyScore": fields.Integer(readonly=True, description="The accuracy score of this information"),
    },
)

error = api.model("Error", {"Success": fields.Boolean(readonly=True), "Message": fields.String(readonly=True)})
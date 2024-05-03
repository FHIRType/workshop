from flask_restx import fields
from .extensions import api

practitioner = api.model(
    "Practitioner",
    {
        "Endpoint": fields.String(
            readonly=True, description="The source endpoint of the information"
        ),
        "DateRetrieved": fields.String(readonly=True, description="The retrieved date"),
        "FullName": fields.String(
            readonly=True, description="The full name of the practitioner"
        ),
        "NPI": fields.String(readonly=True, description="NPI of the practitioner"),
        "FirstName": fields.String(
            readonly=True, description="The first name of the practitioner"
        ),
        "LastName": fields.String(
            readonly=True, description="The last name of the practitioner"
        ),
        "Gender": fields.String(readonly="The gender of the practitioner"),
        "Taxonomy": fields.String(
            readonly=True, description="The practitioner's taxonomy"
        ),
        "GroupName": fields.String(
            readonly=True, description="The group name data of the practitioner"
        ),
        "ADD1": fields.String(readonly=True, description="The first address"),
        "ADD2": fields.String(readonly=True, description="The second address"),
        "City": fields.String(readonly=True, description="The city"),
        "State": fields.String(readonly=True, description="The state"),
        "Zip": fields.String(readonly=True, description="The ZIP code"),
        "Phone": fields.String(
            readonly=True, description="The phone number of the practitioner"
        ),
        "Fax": fields.String(
            readonly=True, description="The fax number of the practitioner"
        ),
        "Email": fields.String(
            readonly=True, description="The email address of the practitioner"
        ),
        "lat": fields.String(readonly=True, description="The latitude"),
        "lng": fields.String(readonly=True, description="The longitude"),
        "LastPracUpdate": fields.String(
            readonly=True,
            description="The last updated date of the Practitioner information",
        ),
        "LastPracRoleUpdate": fields.String(
            readonly=True,
            description="The last updated date of the Practitioner Role information",
        ),
        "LastLocationUpdate": fields.String(
            readonly=True,
            description="The last updated date of the Location information",
        ),
        "AccuracyScore": fields.Integer(
            readonly=True, description="The accuracy score of this information"
        ),
    },
)

error = api.model(
    "Error",
    {"Success": fields.Boolean(readonly=True), "Message": fields.String(readonly=True)},
)

name_fields = api.model(
    "Name", {"first_name": fields.String, "last_name": fields.String}
)

npi_fields = api.model("NPI", {"npi": fields.Nested(name_fields)})

list_fields = api.model(
    "ListData",
    {"data": fields.List(fields.Nested(npi_fields)), "format": fields.String},
)

consensus_fields = api.model(
    "Consensus",
    {
        "collection": fields.List(
            fields.Nested(
                api.model(
                    "Data",
                    {
                        "Endpoint": fields.String(required=True),
                        "DateRetrieved": fields.String(required=True),
                        "FullName": fields.String(required=True),
                        "NPI": fields.Integer(required=True),
                        "FirstName": fields.String(required=True),
                        "LastName": fields.String(required=True),
                        "Gender": fields.String(required=True),
                        "Taxonomy": fields.String(required=False),
                        "GroupName": fields.String(required=False),
                        "ADD1": fields.String(required=True),
                        "ADD2": fields.String(required=False),
                        "City": fields.String(required=False),
                        "State": fields.String(required=False),
                        "Zip": fields.String(required=False),
                        "Phone": fields.Integer(required=False),
                        "Fax": fields.Integer(required=False),
                        "Email": fields.String(required=False),
                        "lat": fields.Float(required=False),
                        "lng": fields.Float(required=False),
                        "Accuracy": fields.Integer(required=False),
                        "LastPracUpdate": fields.String(required=False),
                        "LastPracRoleUpdate": fields.String(required=False),
                        "LastLocationUpdate": fields.String(required=False),
                    },
                )
            )
        ),
    },
)

provider_entry = api.model("Provider Entry", {
    "Endpoint": fields.String(required=True),
    "DateRetrieved": fields.String(required=True),
    "FullName": fields.String(required=True),
    "NPI": fields.Integer(required=True),
    "FirstName": fields.String(required=True),
    "LastName": fields.String(required=True),
    "Gender": fields.String(required=True),
    "Taxonomy": fields.String(required=False),
    "GroupName": fields.String(required=False),
    "ADD1": fields.String(required=True),
    "ADD2": fields.String(required=False),
    "City": fields.String(required=False),
    "State": fields.String(required=False),
    "Zip": fields.String(required=False),
    "Phone": fields.Integer(required=False),
    "Fax": fields.Integer(required=False),
    "Email": fields.String(required=False),
    "lat": fields.Float(required=False),
    "lng": fields.Float(required=False),
    "Accuracy": fields.Integer(required=False),
    "LastPracUpdate": fields.String(required=False),
    "LastPracRoleUpdate": fields.String(required=False),
    "LastLocationUpdate": fields.String(required=False),
})

# Define the collection model which contains a list of provider entries
askai_fields = api.model('Collection', {
    'collection': fields.List(fields.Nested(provider_entry), required=True, description="List of provider entries")
})


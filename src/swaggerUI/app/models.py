from flask_restx import fields
from .extensions import api

practitioner = api.model('Practitioner', {
    'Endpoint': fields.String(readonly=True, description='The task unique identifier'),
    'DateRetrieved': fields.String(required=True, description='The task details'),
    'FullName': fields.String(required=True, description='The task details'),
    'NPI': fields.String(required=True, description='The task details'),
    'FirstName': fields.String(required=True, description='The task details'),
    'LastName': fields.String(required=True, description='The task details'),
    'Gender': fields.String(required=True, description='The task details'),
    'Taxonomy': fields.String(required=True, description='The task details'),
    'GroupName': fields.String(required=True, description='The task details'),
    'Address1': fields.String(required=True, description='The task details'),
    'Address2': fields.String(required=True, description='The task details'),
    'City': fields.String(required=True, description='The task details'),
    'State': fields.String(required=True, description='The task details'),
    'Zip': fields.String(required=True, description='The task details'),
    'Phone': fields.String(required=True, description='The task details'),
    'Fax': fields.String(required=True, description='The task details'),
    'Email': fields.String(required=True, description='The task details'),
    'lat': fields.String(required=True, description='The task details'),
    'lng': fields.String(required=True, description='The task details'),
    'LastPracUpdate': fields.String(required=True, description='The task details'),
    'LastPracRoleUpdate': fields.String(required=True, description='The task details'),
    'LastLocationUpdate': fields.String(required=True, description='The task details'),
    'AccuracyScore': fields.String(required=True, description='The task details'),
})
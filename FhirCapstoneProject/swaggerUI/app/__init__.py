from flask import Flask
from .extensions import api
from .routers import ns
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api.init_app(app)
api.add_namespace(ns)

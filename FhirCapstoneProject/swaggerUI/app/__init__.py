from flask import Flask
from .extensions import api
from .routers import ns


app = Flask(__name__)
api.init_app(app)
api.add_namespace(ns)

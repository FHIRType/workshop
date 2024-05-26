import os
import sys

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.profiler import ProfilerMiddleware

from .extensions import api, limiter
from .routers import ns

app = Flask(__name__)

if os.environ.get("FHIRTYPE_PROFILE") == "1":
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        stream=sys.stderr,
        profile_dir="profile",
        filename_format="{method}.{path}.{elapsed:.0f}ms.{time:.0f}.prof",
    )

CORS(app)
api.init_app(app)
limiter.init_app(app)
api.add_namespace(ns)

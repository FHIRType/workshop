import os
import sys

from FhirCapstoneProject.swaggerUI.app import app

if __name__ == "__main__":
    # print(app.config, file=sys.stderr)
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT"), debug=True)
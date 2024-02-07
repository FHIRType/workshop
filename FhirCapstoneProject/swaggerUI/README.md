# Flask API with Swagger UI
### Description
This is the application for fast APIs and documentation. The application is implemented with [**flask**](https://flask.palletsprojects.com/en/3.0.x/), and [**flask-restx**](https://flask-restx.readthedocs.io/en/latest/) for the Swagger UI.
### How to run it
execute this command on your terminal: ```flask run```
### Exceptional cases
#### 1. Format Errors (Related to Logging.ini issues)
If you run into this kind of issues, run the following command on your terminal:
``$Env:FLASK_APP = "./src/swaggerUI.app"``
#### 2. Powershell Authorization issues
Run the following command on your PowerShell and run ``flask run`` again:
``Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass``
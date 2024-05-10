# Flask API with Swagger UI
### Description
This is the application for fast APIs and documentation. The application is implemented with [**flask**](https://flask.palletsprojects.com/en/3.0.x/), and [**flask-restx**](https://flask-restx.readthedocs.io/en/latest/) for the Swagger UI.
### How to run it
execute this command on your terminal: ```flask run```
### Exceptional cases
#### 1. Format Errors (Related to Logging.ini issues)
If you run into this kind of issues, run the following command on your terminal:

Windows: ``$Env:FLASK_APP = "./FhirCapstoneProject/swaggerUI.app"``

MacOS:  ``export FLASK_APP="./FhirCapstoneProject/swaggerUI.app"``
#### 2. Powershell Authorization issues
Run the following command on your PowerShell and run ``flask run`` again:
``Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass``

## Directory Structure
```
 app
 |
 |  __init__.py
 |  data.py
 |  extensions.py
 |  models.py
 |  parsers.py
 |  routers.py
 |  utils.py
 | 
 └─── static
 |    └─── css
 |         └  app.css
 |
 └─── templates
      |  app.html
      └  list.html
```
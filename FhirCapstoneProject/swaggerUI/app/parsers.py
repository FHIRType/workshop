from flask_restx import reqparse
from FhirCapstoneProject.swaggerUI.app.extensions import get_endpoint_names


# The parser object for GET /getdata endpoint
get_data_parser = reqparse.RequestParser()
get_data_parser.add_argument(
    "first_name", required=True, type=str, help="The first name of the practitioner"
)
get_data_parser.add_argument(
    "last_name", required=True, type=str, help="The last name of the practitioner"
)
get_data_parser.add_argument(
    "npi", required=True, type=str, help="The NPI of the practitioner"
)
get_data_parser.add_argument(
    "endpoint",
    type=str,
    choices=get_endpoint_names(),
    help="The type of the endpoint (default: All)",
)
get_data_parser.add_argument(
    "format",
    type=str,
    choices=("file", "page"),
    help="The type of the returned data - returns JSON format by default.",
)

# The parser object for POST /getdata endpoint
get_list_data_parser = reqparse.RequestParser()
get_list_data_parser.add_argument(
    'endpoint',
    type=str,
    required=True,
    choices=get_endpoint_names(),
    default='All',
    help='Endpoint to fetch data from'
)
get_list_data_parser.add_argument(
    "format",
    required=True,
    type=str,
    choices=("JSON", "File", "Page"),
    default="JSON",
    help="The type of the returned data - returns JSON format by default.",
)


# The parser object for GET /askai endpoint
get_question_parser = reqparse.RequestParser()
get_question_parser.add_argument(
    "question", required=True, type=str, help="Ask a question relating to the bulk data"
)

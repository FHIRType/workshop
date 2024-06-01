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
    required=True,
    default="All",
    help="The type of the endpoint (default: All)",
)
get_data_parser.add_argument(
    "format",
    type=str,
    choices=("JSON", "File", "Page"),
    required=True,
    default="JSON",
    help="The type of the returned data (default: JSON)",
)
get_data_parser.add_argument(
    "consensus",
    type=str,
    choices=("True", "False"),
    required=True,
    default="True",
    help="Append our model's consensus result to your query (default: True)",
)


# The parser object for POST /getdata endpoint
get_list_data_parser = reqparse.RequestParser()
get_list_data_parser.add_argument(
    "endpoint",
    type=str,
    required=True,
    choices=get_endpoint_names(),
    default="All",
    help="Endpoint to fetch data from",
)
get_list_data_parser.add_argument(
    "format",
    required=True,
    type=str,
    choices=("JSON", "File", "Page"),
    default="JSON",
    help="The type of the returned data - returns JSON format by default.",
)
get_list_data_parser.add_argument(
    "consensus",
    type=str,
    choices=("True", "False"),
    required=True,
    default="False",
    help="Append our model's consensus result to your query",
)


# The parser object for GET /askai endpoint
get_question_parser = reqparse.RequestParser()
get_question_parser.add_argument(
    "question", required=True, type=str, help="Ask a question relating to the bulk data"
)

# The parser object for POST /askai endpoint
get_group_parser = reqparse.RequestParser()
get_group_parser.add_argument(
    "question", required=True, type=str, help="Post data for AI to group"
)

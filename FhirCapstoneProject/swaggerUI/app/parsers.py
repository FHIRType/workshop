from flask_restx import reqparse

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
    choices=("Humana", "Kaiser", "Cigna", "Centene", "PacificSource"),
    help="The type of the endpoint (default: All)"
)
get_data_parser.add_argument(
    "format",
    type=str,
    choices=("file", "page"),
    help="The type of the returned data - returns JSON format by default.",
)


get_question_parser = reqparse.RequestParser()
get_question_parser.add_argument(
    "question", required=True, type=str, help="Ask a question relating to the bulk data"
)

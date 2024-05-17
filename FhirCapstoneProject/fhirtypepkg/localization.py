dictionary = {
    "APP_APP_ID": "app_id",
    "APP_API_BASE": "api_base",
    "HL7_DEFINITION_NPI": "http://hl7.org/fhir/sid/us-npi",
    "PRACTITIONER_FAMILY_NAME": "family",
    "PRACTITIONER_GIVEN_NAME": "given",
    "PRACTITIONER_IDENTIFIER": "identifier",
    "RESOURCE_PRACTITIONER": "practitioner",
    "RESOURCE_PRACTITIONER_ROLE": "practitionerrole",
    "RESOURCE_LOCATION": "location",
    "RESOURCE_ORGANIZATION": "organization",
    "PATH_PRACTITIONER": "Practitioner",
    "PATH_PRACTITIONER_ROLE": "PractitionerRole",
    "PATH_LOCATION": "Location",
    "PATH_ORGANIZATION": "Organization",
}

thesaurus = {
    "APP_ID": dictionary["APP_APP_ID"],
    "APP ID": dictionary["APP_APP_ID"],
    "API_BASE": dictionary["APP_API_BASE"],
    "API BASE": dictionary["APP_API_BASE"],
    "FAMILY NAME": dictionary["PRACTITIONER_FAMILY_NAME"],
    "FAMILY": dictionary["PRACTITIONER_FAMILY_NAME"],
    "LAST NAME": dictionary["PRACTITIONER_FAMILY_NAME"],
    "LAST": dictionary["PRACTITIONER_FAMILY_NAME"],
    "GIVEN NAME": dictionary["PRACTITIONER_GIVEN_NAME"],
    "GIVEN": dictionary["PRACTITIONER_GIVEN_NAME"],
    "FIRST NAME": dictionary["PRACTITIONER_GIVEN_NAME"],
    "FIRST": dictionary["PRACTITIONER_GIVEN_NAME"],
    "IDENTIFIER": dictionary["PRACTITIONER_IDENTIFIER"],
    "NPI": dictionary["PRACTITIONER_IDENTIFIER"],
    "PRAC NPI": dictionary["PRACTITIONER_IDENTIFIER"],
    "NPI CODE": dictionary["HL7_DEFINITION_NPI"],
    "NPI DEFINITION": dictionary["HL7_DEFINITION_NPI"],
    "PRACTITIONER": dictionary["RESOURCE_PRACTITIONER"],
    "TITLECASE PRACTITIONER": dictionary["PATH_PRACTITIONER"],
    "TITLE CASE PRACTITIONER": dictionary["PATH_PRACTITIONER"],
    "PRACTITIONER ROLE": dictionary["RESOURCE_PRACTITIONER_ROLE"],
    "TITLECASE PRACTITIONER ROLE": dictionary["PATH_PRACTITIONER_ROLE"],
    "TITLE CASE PRACTITIONER ROLE": dictionary["PATH_PRACTITIONER_ROLE"],
    "TITLECASE PRACTITIONERROLE": dictionary["PATH_PRACTITIONER_ROLE"],
    "TITLE CASE PRACTITIONERROLE": dictionary["PATH_PRACTITIONER_ROLE"],
    "LOCATION": dictionary["RESOURCE_LOCATION"],
    "TITLECASE LOCATION": dictionary["PATH_LOCATION"],
    "TITLE CASE LOCATION": dictionary["PATH_LOCATION"],
    "ORGANIZATION": dictionary["RESOURCE_ORGANIZATION"],
    "TITLECASE ORGANIZATION": dictionary["PATH_ORGANIZATION"],
    "TITLE CASE ORGANIZATION": dictionary["PATH_ORGANIZATION"],
}


def localize(text: str):
    """
    Convert text to uppercase and look it up in the dictionary or thesaurus.

    Parameters:
       text (str): The text to localize.

    Returns:
       str: The localized text from the dictionary or thesaurus.

    Raises:
       KeyError: If the text is not found in either the dictionary or thesaurus.
    """
    text = text.upper()

    if text in dictionary:
        return dictionary[text]

    if text in thesaurus:
        return thesaurus[text]

    raise KeyError(text)

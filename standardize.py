# Author: Hla Htun
# Description: Returns a list of important values from the resource object passed to it
import re


def is_valid_taxonomy(taxonomy):
    # Define a regular expression pattern for the desired format
    pattern = re.compile(r'^.{9}X$')

    # Check if the string matches the pattern
    return bool(pattern.match(taxonomy))


# Author: Hla Htun
# string is the input string to be normalized
# d_type is the type of data the string is supposed to be
# returns the normalized string
def normalize(string, d_type):
    if d_type == "degree":
        return string.strip(", ")

    # TODO: more datatype can be specified here if needed in future


def Kaiser_getTaxonomyAndDisplay(qualifications):
    for qualification in qualifications:
        value = str(qualification.code.coding[0].code)
        if is_valid_taxonomy(value):
            return value, qualification.code.coding[0].display

    return None, None


def Kaiser_getLicenseNumber(qualifications):
    licenses = []

    for qualification in qualifications:
        license_details = {}
        if qualification.extension:
            for extension in qualification.extension:
                if extension.valueCodeableConcept:
                    license_details["state"] = extension.valueCodeableConcept.coding[0].display

        if qualification.identifier:
            license_details["license"] = qualification.identifier[0].value

        if qualification.period:
            period = {
                qualification.period.start.isostring,
                qualification.period.end.isostring
            }
            license_details["period"] = period

        # only append if not empty
        if license_details:
            licenses.append(license_details)

    if licenses:
        return licenses
    else:
        return None


def Kaiser_getQualifications(qualifications):
    taxonomy, display = Kaiser_getTaxonomyAndDisplay(qualifications)
    qualifications = {
        "taxonomy": taxonomy,
        "display": display,
    }
    return qualifications


def get_practitioner_name(resource, endpoint):
    first_name = None
    last_name = None
    degree = None
    prefix = None
    full_name = None
    if endpoint == "kaiser":
        if resource.name[0]:
            if resource.name[0].given[0]:
                first_name = resource.name[0].given[0]

            if resource.name[0].family:
                last_name = resource.name[0].family

            if resource.name[0].text:
                degree = normalize(resource.name[0].text, "degree")

        return {"first_name": first_name, "last_name": last_name, "degree": degree}

    elif endpoint == "humana":
        # "first_name": res.name[0].family if res.name and res.name[0] and res.name[0].family else None,
        # "last_name": res.name[0].given[0] if res.name and res.name[0] and res.name[0].given else None,
        # "prefix": res.name[0].prefix[0] if res.name and res.name[0] and res.name[0].prefix else None,
        # "full_name
        if resource.name[0]:
            if resource.name[0].given[0]:
                first_name = resource.name[0].given[0]

            if resource.name[0].family:
                last_name = resource.name[0].family

            if resource.name[0].prefix[0]:
                prefix = resource.name[0].prefix[0]

            if resource.name[0].text:
                full_name = resource.name[0].text

        return { "first_name": first_name, "last_name": last_name, "prefix": prefix, "full_name": full_name }

    return {"first_name": first_name, "last_name": last_name, "degree": degree}


def Kaiser_getIdentifier(identifier):
    provider_number = None
    npi = None
    for identities in identifier:
        if identities.type and identities.value:
            provider_number = identities.value

        if identities.value and not identities.type:
            npi = identities.value

    return { "npi": npi, "provider_number": provider_number }


def getKaiserData(resource):
    name = get_practitioner_name(resource, "kaiser")
    qualifications = Kaiser_getQualifications(resource.qualification)
    licenses = Kaiser_getLicenseNumber(resource.qualification)
    identifier = Kaiser_getIdentifier(resource.identifier)

    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "active": resource.active,
        "name": name,
        "gender": resource.gender,
        "identifier": identifier,
        "qualification": qualifications,
        "licenses": licenses
    }


def getHumanaData(resource):
    name = get_practitioner_name(resource, "humana")
    return {
        "id": resource.id,
        "last_updated": resource.meta.lastUpdated.isostring,
        "active": resource.active,
        "name": name,
        "gender": resource.gender,
        "npi": resource.identifier[0].value if resource.identifier[0].value else None
    }

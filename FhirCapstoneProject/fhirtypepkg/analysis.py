# Authors: Iain Richey, Hla Htun
####################
# This file contains the different analysis models for the different types of queries
####################
from datetime import datetime as dtime
import numpy as np
from dateutil import parser

####################
# This function takes in a set of queries to the various endpoints, and analyses them for the most likely results
####################

def predict(queries) -> dict: #will return whatever our container class is 
    unique_features = {}
    today = dtime.today()
    for query in queries: #loop through each endpoints query

        if len(queries) == 0:
            return queries[0].id, queries

        max_fea = {}
        for query in queries:
            last_updated = parser.parse(query.get("LastPracUpdate", ""))
            if not last_updated:
                continue

            time_diff = (today.date() - last_updated.date()).days
            
            time_diff /= 100
            if query != None: #some endpoints might not have the person

                #matches unique features (ie no repeats)
                for index, (key, value) in enumerate(query.items()):

                    if key not in unique_features: #add each unique feature to our dict
                        unique_features[key] = {}

                    if value in unique_features[key]:
                        unique_features[key][value] += time_diff

                    else: 
                        unique_features[key][value] = time_diff

    highest_features = [] #dict of the highest voted result for each feature
    highest_features = {feature: max(options, key=options.get) for feature, options in unique_features.items()}

    highest_features["Accuracy"] = 1
    highest_features["Endpoint"] = "Concensus"

    return highest_features

def logistic(last_updated):
    return 1 / (1 + np.exp(-last_updated))

testMich = [
  {
    "Endpoint": "Humana",
    "DateRetrieved": "2024-02-29T04:47:16Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-08-06T08:26:02Z",
    "GroupName": None,
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-08-05T08:53:45Z",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-08-06T08:12:10Z"
  },
  {
    "Endpoint": "Humana",
    "DateRetrieved": "2024-02-29T04:47:16Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-08-06T08:26:02Z",
    "GroupName": None,
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-08-05T10:16:17Z",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-08-06T08:12:10Z"
  },
  {
    "Endpoint": "Humana",
    "DateRetrieved": "2024-02-29T04:47:16Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-08-06T08:26:02Z",
    "GroupName": None,
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-08-05T12:07:47Z",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-08-06T08:12:10Z"
  },
  {
    "Endpoint": "Humana",
    "DateRetrieved": "2024-02-29T04:47:16Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-08-06T08:26:02Z",
    "GroupName": None,
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-08-05T17:30:40Z",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-08-06T08:12:10Z"
  },
  {
    "Endpoint": "Humana",
    "DateRetrieved": "2024-02-29T04:47:16Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-08-06T08:26:02Z",
    "GroupName": None,
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-08-05T05:31:10Z",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-08-06T08:12:10Z"
  },
  {
    "Endpoint": "Kaiser",
    "DateRetrieved": "2024-02-29T04:47:22Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2024-01-05T01:44:29-08:00",
    "GroupName": "Willamette Valley Family Center, LLC",
    "Taxonomy": None,
    "LastPracRoleUpdate": "2024-01-05T02:15:54-08:00",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045-2329",
    "Phone": 8556328280,
    "Fax": 5036577676,
    "Email": None,
    "lat": 45.354828,
    "lng": -122.604025,
    "LastLocationUpdate": "2024-01-05T01:09:58-08:00"
  },
  {
    "Endpoint": "PacificSource",
    "DateRetrieved": "2024-02-29T04:47:24Z",
    "Accuracy": -1,
    "FullName": "Dykstra, Michelle",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2023-09-12T21:36:49-07:00",
    "GroupName": "Unknown",
    "Taxonomy": None,
    "LastPracRoleUpdate": "2023-09-12T21:38:36-07:00",
    "ADD1": "610 Jefferson St",
    "ADD2": "Optional",
    "City": "Oregon City",
    "State": "OR",
    "Zip": "97045",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": None,
    "lng": None,
    "LastLocationUpdate": "2023-09-12T21:38:36-07:00"
  }
]


test_prac = [
    {
        "fname": "John",
        "lname": "Weaver",
        "npi": "123456",
        "age": 37,
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "fname": "Johnny",
        "lname": "Weaver",
        "npi": "123456",
        "age": 22,
        "gender": "Male",
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
    {
        "fname": "Iain",
        "lname": "Richey",
        "npi": "137681",
        "age": 37,
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "fname": "John",
        "lname": "Weaver",
        "npi": "123456",
        "age": 40,
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
]

test_prac_role = [
    {
        "id": 1578,
        "active": True,
        "identifier": "1",
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
    {
        "id": 1578,
        "active": True,
        "identifier": "1",
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "id": 1578,
        "active": False,
        "identifier": "2",
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "id": 1578,
        "active": False,
        "identifier": "1",
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
]

test_location = [
    {
        "id": 137,
        "status": "active",
        "phone": "581-234-9872",
        "address": "1234 fake street",
        "name": "Jerry bone emporium",
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "id": 137,
        "status": "active",
        "phone": "581-234-9872",
        "address": "1234 fake street",
        "name": "whitebird",
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
    {
        "id": 129,
        "status": "active",
        "phone": "581-234-9872",
        "address": "872 real ave",
        "name": "Jerry bone emporium",
        "last_updated": "2023-05-16T10:30:00+05:00",
    },
    {
        "id": 137,
        "status": "active",
        "phone": "581-234-9872",
        "address": "993 not real lane",
        "name": "Jerry bone emporium",
        "last_updated": "2022-11-15T23:05:21-08:00",
    },
]

test3 = [
    {
        "id": "1c36b08d-10d8-4569-a014-baa65c754570",
        "last_updated": "2023-10-20T00:27:23-07:00",
        "active": True,
        "name": {
            "first_name": "Brandon",
            "middle_name": None,
            "last_name": "Bianchini",
            "prefix": None,
            "full_name": None,
            "qualification": "PA",
        },
        "gender": "male",
        "identifier": {
            "npi": "1700158326",
            "provider_number": "EPDM-IND-0000074279",
        },
        "qualification": {
            "taxonomy": "363A00000X",
            "display": "Physician Assistant",
        },
        "licenses": None,
    },
    {
        "id": "1c36b08d-10d8-4569-a014-baa65c754571",
        "last_updated": "2023-11-20T00:27:23-07:00",
        "active": True,
        "name": {
            "first_name": "Iain",
            "middle_name": None,
            "last_name": "Bianchini",
            "prefix": None,
            "full_name": None,
            "qualification": "PA",
        },
        "gender": "male",
        "identifier": {
            "npi": "1700158326",
            "provider_number": "EPDM-IND-0000074279",
        },
        "qualification": {
            "taxonomy": "363A00000X",
            "display": "Physician Assistant",
        },
        "licenses": None,
    },
    {
        "id": "1c36b08d-10d8-4569-a014-baa65c754572",
        "last_updated": "2023-10-20T00:27:23-07:00",
        "active": True,
        "name": {
            "first_name": "Brandon",
            "middle_name": None,
            "last_name": "Bianchini",
            "prefix": None,
            "full_name": None,
            "qualification": "PA",
        },
        "gender": "male",
        "identifier": {
            "npi": "1700158326",
            "provider_number": "EPDM-IND-0000074279",
        },
        "qualification": {
            "taxonomy": "363A00000X",
            "display": "Physician Assistant",
        },
        "licenses": None,
    },
    {
        "id": "1c36b08d-10d8-4569-a014-baa65c754573",
        "last_updated": "2023-11-30T00:27:23-07:00",
        "active": True,
        "name": {
            "first_name": "Iain",
            "middle_name": None,
            "last_name": "Bianchini",
            "prefix": None,
            "full_name": None,
            "qualification": "PA",
        },
        "gender": "male",
        "identifier": {
            "npi": "1700158326",
            "provider_number": "EPDM-IND-0000074279",
        },
        "qualification": {
            "taxonomy": "363A00000X",
            "display": "Physician Assistant",
        },
        "licenses": None,
    },
    {
        "id": "1c36b08d-10d8-4569-a014-baa65c754574",
        "last_updated": "2023-08-01T00:27:23-07:00",
        "active": True,
        "name": {
            "first_name": "Brandon",
            "middle_name": None,
            "last_name": "Bianchini",
            "prefix": None,
            "full_name": None,
            "qualification": "PA",
        },
        "gender": "male",
        "identifier": {
            "npi": "1700158326",
            "provider_number": "EPDM-IND-0000074279",
        },
        "qualification": {
            "taxonomy": "363A00000X",
            "display": "Physician Assistant",
        },
        "licenses": None,
    },
]

test4 = [
    {
        "id": "d80d44a4-3a18-4709-8bcc-de34ac61661d",
        "language": "en-US",
        "last_updated": "2023-11-15T23:12:45.057-08:00",
        "meta": {
            "lastUpdated": "2023-11-15T23:12:45.057-08:00",
            "source": "HPPDM_ADAPTER",
            "versionId": "4",
        },
        "extension": [
            {
                "url": "https://healthy.kaiserpermanente.org/display-indicator",
                "valueBoolean": True,
            }
        ],
        "active": True,
        "communication": [
            {
                "extension": [
                    {
                        "url": "http://tools.ietf.org/html/bcp47",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "30",
                                    "display": "General professional proficiency",
                                },
                                {
                                    "code": "spa",
                                    "display": "Spanish",
                                    "system": "http://tools.ietf.org/html/bcp47",
                                },
                            ]
                        },
                    }
                ],
                "text": "Spanish",
            },
            {
                "extension": [
                    {
                        "url": "http://tools.ietf.org/html/bcp47",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "30",
                                    "display": "General professional proficiency",
                                },
                                {
                                    "code": "eng",
                                    "display": "English",
                                    "system": "http://tools.ietf.org/html/bcp47",
                                },
                            ]
                        },
                    }
                ],
                "text": "English",
            },
        ],
        "gender": "male",
        "identifier": [
            {
                "system": "http://hl7.org/fhir/sid/us-npi",
                "use": "usual",
                "value": "1477512051",
            },
            {
                "system": "https://healthy.kaiserpermanente.org",
                "type": {"coding": [{"code": "PRN", "display": "Provider number"}]},
                "value": "EPDM-IND-0000003661",
            },
            {
                "system": "https://healthy.kaiserpermanente.org",
                "type": {"coding": [{"code": "RI", "display": "Resource identifier"}]},
                "value": "2942776",
            },
        ],
        "name": [
            {
                "family": "Barnatan",
                "given": ["Marcos F"],
                "text": "Marcos F Barnatan, MD",
            }
        ],
        "qualification": [
            {
                "extension": [
                    {
                        "url": "http://build.fhir.org/ig/HL7/davinci-pdex-plan-net/CodeSystem-QualificationStatusCS",
                        "valueCode": "active",
                    },
                    {
                        "url": "https://www.usps.com/",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "OR",
                                    "display": "Oregon",
                                    "system": "https://www.usps.com/",
                                }
                            ]
                        },
                    },
                ],
                "code": {
                    "coding": [
                        {
                            "code": "unknown",
                            "display": "Unknown",
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                        }
                    ],
                    "text": "The value is expected to exist but is not known.",
                },
                "identifier": [
                    {
                        "type": {
                            "coding": [
                                {
                                    "code": "LN",
                                    "display": "License number",
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                }
                            ]
                        },
                        "value": "MD23484",
                    }
                ],
            },
            {
                "extension": [
                    {
                        "url": "http://build.fhir.org/ig/HL7/davinci-pdex-plan-net/CodeSystem-QualificationStatusCS",
                        "valueCode": "active",
                    },
                    {
                        "url": "https://www.usps.com/",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "WA",
                                    "display": "Washington",
                                    "system": "https://www.usps.com/",
                                }
                            ]
                        },
                    },
                ],
                "code": {
                    "coding": [
                        {
                            "code": "unknown",
                            "display": "Unknown",
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                        }
                    ],
                    "text": "The value is expected to exist but is not known.",
                },
                "identifier": [
                    {
                        "period": {
                            "end": "2024-10-08T00:00:00-07:00",
                            "start": "2002-02-22T00:00:00-08:00",
                        },
                        "type": {
                            "coding": [
                                {
                                    "code": "LN",
                                    "display": "License number",
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                }
                            ]
                        },
                        "value": "MD00040854",
                    }
                ],
                "period": {
                    "end": "2024-10-08T00:00:00-07:00",
                    "start": "2002-02-22T00:00:00-08:00",
                },
            },
            {
                "code": {
                    "coding": [
                        {
                            "code": "2086S0129X",
                            "display": "Vascular Surgery Physician",
                            "system": "http://nucc.org/provider-taxonomy",
                        }
                    ],
                    "text": "Qualification Specialty Name Details :",
                }
            },
            {
                "code": {
                    "coding": [
                        {
                            "code": "Education",
                            "display": "Facultad De Medicina - Universidad Complutense De Madrid (Madrid, Spain)",
                            "system": "http://nucc.org/provider-taxonomy",
                        }
                    ]
                }
            },
            {
                "code": {
                    "coding": [
                        {
                            "code": "Certification",
                            "display": "Gen Vascular-AB Surgery",
                            "system": "http://nucc.org/provider-taxonomy",
                        }
                    ]
                }
            },
        ],
        "resourceType": "Practitioner",
    },
    {
        "id": "dir-CcB4wRrOu1K4uys0sGE7EGV4k0qR79bvy8JInEx1up",
        "language": "en",
        "last_updated": "2023-09-01T23:29:06.801000+00:00",
        "meta": {
            "lastUpdated": "2023-09-01T23:29:06.801000+00:00",
            "profile": [
                "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Practitioner"
            ],
            "source": "urn:evernorth:hi2:source:gov:madir",
            "versionId": "9000000000000",
        },
        "active": True,
        "birthDate": "1963-10-08",
        "gender": "male",
        "identifier": [
            {
                "system": "http://hl7.org/fhir/sid/us-npi",
                "type": {
                    "coding": [
                        {
                            "code": "NPI",
                            "display": "National provider identifier",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "version": "2.9.0",
                        }
                    ]
                },
                "value": "1477512051",
            },
            {
                "system": "https://fhir.evernorth-fhir-prod.aws.cignacloud.com/r4",
                "use": "usual",
                "value": "8451644a0987aa89be9f0dd6b3307e16",
            },
        ],
        "name": [
            {"family": "BARNATAN", "given": ["MARCOS"], "text": "MARCOS BARNATAN"}
        ],
        "qualification": [
            {
                "code": {
                    "coding": [
                        {
                            "code": "MD",
                            "display": "Doctor of Medicine",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                            "version": "2.1.0",
                        }
                    ]
                }
            }
        ],
        "resourceType": "Practitioner",
    },
    {
        "id": "753433",
        "language": "en-US",
        "last_updated": "2023-12-15T18:16:35.000+00:00",
        "meta": {
            "lastUpdated": "2023-12-15T18:16:35.000+00:00",
            "profile": [
                "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Practitioner"
            ],
            "source": "Centene",
        },
        "text": {
            "div": '<div xmlns="http://www.w3.org/1999/xhtml">SPECIALIST</div>',
            "status": "extensions",
        },
        "active": True,
        "communication": [
            {
                "coding": [
                    {
                        "code": "Spanish",
                        "system": "http://hl7.org/fhir/ValueSet/languages",
                    }
                ]
            }
        ],
        "gender": "male",
        "identifier": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                "type": {
                    "coding": [
                        {
                            "code": "MCR",
                            "display": "Practitioner Medicare number",
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        }
                    ]
                },
                "value": "R131466",
            },
            {"id": "pracId", "use": "official", "value": "753433"},
            {"id": "healthNetLegacyPhyId", "use": "official", "value": "P092925"},
        ],
        "name": [
            {
                "family": "Barnatan",
                "given": ["Marcos", "F"],
                "text": "Marcos F Barnatan",
                "use": "official",
            }
        ],
        "qualification": [
            {
                "code": {
                    "coding": [
                        {
                            "code": "MD 000000023484",
                            "display": "Other Service Provider",
                            "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/practitioner-qualification",
                        }
                    ]
                },
                "issuer": {"display": "Oregon", "reference": "Oregon"},
                "period": {"end": "2023-12-31T00:00:00+00:00"},
            },
            {
                "code": {
                    "coding": [
                        {
                            "code": "MD00040854",
                            "display": "Other Service Provider",
                            "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/practitioner-qualification",
                        }
                    ]
                },
                "issuer": {"display": "Washington", "reference": "Washington"},
                "period": {"end": "2022-10-08T00:00:00+00:00"},
            },
        ],
        "resourceType": "Practitioner",
    },
]

if __name__ == "__main__":
    res2 = predict(testMich)
    print(res2)

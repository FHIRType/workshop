prac_sample_resource = {
    "id": "279270",
    "language": "en-US",
    "meta": {
        "extension": [
            {"url": "http://centene.com/prtr/vendor", "valueBoolean": False},
            {"url": "http://centene.com/prtr/directory-display", "valueBoolean": True},
        ],
        "lastUpdated": "2021-06-22T11:03:51.000+00:00",
        "profile": [
            "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Practitioner"
        ],
        "source": "MHN",
    },
    "active": True,
    "address": [
        {
            "city": "OREGON CITY",
            "country": "USA",
            "district": "CLACKAMAS",
            "line": ["610 JEFFERSON ST"],
            "postalCode": "97045-2329",
            "state": "OR",
            "text": "610 JEFFERSON ST,OREGON CITY,OR,97045-2329",
            "type": "postal",
            "use": "work",
        }
    ],
    "gender": "female",
    "identifier": [
        {
            "assigner": {
                "display": "Organization MHN",
                "reference": "Organization/MHN",
            },
            "system": "http://hl7.org/fhir/sid/us-npi",
            "type": {
                "coding": [
                    {
                        "code": "NPI",
                        "display": "National provider identifier",
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                    }
                ]
            },
            "value": "1013072586",
        }
    ],
    "name": [
        {"family": "DYKSTRA", "given": ["MICHELLE", "L"], "text": "DYKSTRA, MICHELLE L"}
    ],
    "qualification": [
        {
            "code": {
                "coding": [
                    {
                        "code": "PHD",
                        "display": "Doctorate, PH",
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                    }
                ],
                "text": "Doctorate, PH",
            },
            "issuer": {
                "display": "Practitioner/279270",
                "reference": "Practitioner/279270",
            },
            "period": {"start": "1992"},
        },
        {
            "code": {
                "coding": [
                    {
                        "code": "103TC2200X",
                        "display": "Psychologist (Clinical Child & Adolescent)",
                        "system": "http://nucc.org/provider-taxonomy",
                    }
                ],
                "text": "Psychologist (Clinical Child & Adolescent)",
            },
            "issuer": {
                "display": "Practitioner/279270",
                "reference": "Practitioner/279270",
            },
        },
    ],
    "telecom": [
        {"system": "phone", "use": "work", "value": "503-657-7235"},
        {"system": "fax", "use": "work", "value": "503-657-7676"},
        {"system": "email", "use": "work", "value": "BILLING@WVFC.NET"},
    ],
    "resourceType": "Practitioner",
}

prac_sample_output = {
    "Endpoint": "Centene",
    "DateRetrieved": "2024-02-16T19:12:42Z",
    "Accuracy": -1.0,
    "FullName": "DYKSTRA, MICHELLE L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
}

prac_role_sample_resource = {
    "id": "dir-ObTJsLziptI5LKNVIP25pLQ5znAw6pGmRBT8uMx1up",
    "language": "en",
    "meta": {
        "lastUpdated": "2023-11-09T03:23:38.102000+00:00",
        "profile": [
            "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-PractitionerRole"
        ],
        "security": [
            {
                "code": "MH",
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            },
            {
                "code": "R",
                "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
            },
        ],
        "source": "urn:evernorth:hi2:source:gov:madir",
        "versionId": "9000000000000",
    },
    "extension": [
        {
            "extension": [
                {
                    "url": "acceptingPatients",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "code": "newpt",
                                "display": "Accepting",
                                "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/AcceptingPatientsCS",
                                "version": "1.0.0",
                            }
                        ]
                    },
                }
            ],
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/newpatients",
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "code": "PHD",
                                "display": "Doctor of Philosophy",
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                                "version": "2.1.0",
                            }
                        ]
                    },
                },
                {"url": "status", "valueCode": "active"},
            ],
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/qualification",
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/network-reference",
            "valueReference": {
                "reference": "Organization/dir-7462mAXxGHgr2wAiYT07zYH27L2xedzvyChjzgx1up",
                "type": "Organization",
            },
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "code": "OTH",
                                "display": "other",
                                "system": "http://terminology.hl7.org/CodeSystem/v3-NullFlavor",
                                "version": "2.0.0",
                            }
                        ]
                    },
                },
                {"url": "status", "valueCode": "active"},
            ],
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/qualification",
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/network-reference",
            "valueReference": {
                "reference": "Organization/dir-C8rm3AYYkV4o7EpCKHENR68rxYupJdF5xsdCkIx1up",
                "type": "Organization",
            },
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/network-reference",
            "valueReference": {
                "reference": "Organization/dir-Gd3xzzdpnQ8X9C1zv35zCThlpMHr74xUh7156cx1up",
                "type": "Organization",
            },
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "code": "103T00000X",
                                "display": "Psychologist",
                                "system": "http://nucc.org/provider-taxonomy",
                                "version": "1.0.0",
                            }
                        ]
                    },
                },
                {"url": "status", "valueCode": "active"},
            ],
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/qualification",
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/network-reference",
            "valueReference": {
                "reference": "Organization/dir-ysLhc89PpF4wXxfUCQvTutbttByxEU3w2sEaS0x1up",
                "type": "Organization",
            },
        },
    ],
    "active": True,
    "code": [
        {
            "coding": [
                {
                    "code": "ph",
                    "display": "Physician",
                    "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/ProviderRoleCS",
                    "version": "1.0.0",
                }
            ]
        }
    ],
    "healthcareService": [
        {
            "reference": "HealthcareService/dir-pWsDhGOvTC9Zd8U160LQXnb1ebxXtg6PqFG6tkx1up",
            "type": "HealthcareService",
        }
    ],
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
            "value": "1013072586",
        },
        {
            "system": "https://fhir.evernorth-fhir-prod.aws.cignacloud.com/r4",
            "use": "usual",
            "value": "312a8c01fd32ce0e51feef8d7a3cdd4d",
        },
    ],
    "location": [
        {
            "reference": "Location/dir-gdBDYxyTIFYaurFFjRf6N1hbUEEUmsQc7CxwoMx1up",
            "type": "Location",
        }
    ],
    "organization": {
        "extension": [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                "valueCode": "unknown",
            }
        ]
    },
    "period": {"end": "2099-12-31", "start": "1900-01-01"},
    "practitioner": {
        "reference": "Practitioner/dir-mrykxhwOuxGD4di3udpYHx2Jz7Nzjuwk6MDUtox1up",
        "type": "Practitioner",
    },
    "specialty": [
        {
            "coding": [
                {
                    "code": "103T00000X",
                    "display": "Psychologist",
                    "system": "http://nucc.org/provider-taxonomy",
                }
            ]
        }
    ],
    "telecom": [{"rank": 1, "system": "phone", "value": "5036577235"}],
    "resourceType": "PractitionerRole",
}

prac_role_sample_output = {
    "Endpoint": "Cigna",
    "DateRetrieved": "2024-02-16T19:13:48Z",
    "Accuracy": -1.0,
    "FullName": "DYKSTRA, MICHELLE L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "roles": [
        {
            "GroupName": None,
            "Taxonomy": "103T00000X",
            "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
        }
    ],
}

prac_loc_sample_resource = {
    "id": "dir-gdBDYxyTIFYaurFFjRf6N1hbUEEUmsQc7CxwoMx1up",
    "language": "en",
    "meta": {
        "lastUpdated": "2023-09-12T23:46:56.563Z",
        "profile": [
            "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Location"
        ],
        "source": "urn:evernorth:hi2:source:gov:madir",
        "versionId": "9000000000001",
    },
    "extension": [
        {
            "extension": [
                {
                    "url": "acceptingPatients",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "code": "newpt",
                                "display": "Accepting",
                                "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/AcceptingPatientsCS",
                                "version": "1.0.0",
                            }
                        ]
                    },
                }
            ],
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/newpatients",
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/accessibility",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "code": "handiaccess",
                        "display": "handicap accessible",
                        "system": "http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/AccessibilityCS",
                        "version": "1.0.0",
                    }
                ]
            },
        },
    ],
    "address": {
        "city": "OREGON CITY",
        "country": "UNITED STATES",
        "district": "CLACKAMAS",
        "line": ["610 JEFFERSON ST"],
        "postalCode": "97045-2329",
        "state": "OR",
    },
    "identifier": [
        {
            "value": "2317636610 JEFFERSON STOREGON CITYCLACKAMASOR970452329UNITED STATES"
        },
        {
            "system": "https://fhir.evernorth-fhir-prod.aws.cignacloud.com/r4",
            "use": "usual",
            "value": "e67628e814dd77d13edd155f57cb1524",
        },
    ],
    "name": "610 JEFFERSON ST-97045",
    "position": {"latitude": 45.3403, "longitude": -122.5778},
    "status": "active",
    "telecom": [{"system": "phone", "use": "work", "value": "5036577235"}],
    "resourceType": "Location",
}

prac_loc_sample_output = {
    "Endpoint": "Cigna",
    "DateRetrieved": "2024-02-16T18:32:55Z",
    "Accuracy": -1.0,
    "FullName": "DYKSTRA, MICHELLE L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "roles": [
        {
            "GroupName": None,
            "Taxonomy": "103T00000X",
            "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
            "locations": [
                {
                    "ADD1": "610 JEFFERSON ST",
                    "ADD2": "Optional",
                    "City": "OREGON CITY",
                    "State": "OR",
                    "Zip": "97045-2329",
                    "Phone": 5036577235,
                    "Fax": None,
                    "Email": None,
                    "lat": 45.3403,
                    "lng": -122.5778,
                    "LastLocationUpdate": "2023-09-12T23:46:56Z",
                }
            ],
        }
    ],
}

prac_all_prac_res_sample_output = {
    "Endpoint": "Cigna",
    "DateRetrieved": "2024-02-16T18:32:55Z",
    "Accuracy": -1.0,
    "FullName": "DYKSTRA, MICHELLE L",
    "NPI": 1013072586,
    "FirstName": "Michelle",
    "LastName": "Dykstra",
    "Gender": "Female",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "Taxonomy": "103T00000X",
    "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
    "GroupName": None,
    "ADD1": "610 JEFFERSON ST",
    "ADD2": "Optional",
    "City": "OREGON CITY",
    "State": "OR",
    "Zip": "97045-2329",
    "Phone": 5036577235,
    "Fax": None,
    "Email": None,
    "lat": 45.3403,
    "lng": -122.5778,
    "LastLocationUpdate": "2023-09-12T23:46:56Z",
}

analysis_output = {
    'Endpoint': 'Consensus', 
    'DateRetrieved': '2024-02-29T04:47:16Z', 
    'Accuracy': 1, 
    'FullName': 'Dykstra, Michelle L', 
    'NPI': 1013072586, 
    'FirstName': 'Michelle', 
    'LastName': 'Dykstra', 
    'Gender': 'Female', 
    'LastPracUpdate': '2023-08-06T08:26:02Z', 
    'GroupName': None, 
    'Taxonomy': None, 
    'LastPracRoleUpdate': '2023-08-05T08:53:45Z', 
    'ADD1': '610 Jefferson St', 
    'ADD2': 'Optional', 
    'City': 'Oregon City', 
    'State': 'OR', 
    'Zip': '97045', 
    'Phone': 5036577235, 
    'Fax': None, 
    'Email': None, 
    'lat': None, 
    'lng': None, 
    'LastLocationUpdate': '2023-08-06T08:12:10Z'
}

analysis_test_input = [
    {
        "Endpoint": "Humana",
        "DateRetrieved": "2024-02-29T04:47:16Z",
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

accuracy_consensus = {
        "Endpoint": "",
        "DateRetrieved": "2/1/2024",
        "FullName": "Dykstra, Michelle L.",
        "NPI": "1013072586",
        "FirstName": "Michelle",
        "LastName": "Dykstra",
        "Gender": "F",
        "Taxonomy": "103T00000X",
        "GroupName": "Willamette Valley Family Center",
        "ADD1": "610 Jefferson St",
        "ADD2": "",
        "City": "Oregon City",
        "State": "OR",
        "Zip": "970452329",
        "Phone": "5036577235",
        "Fax": "5036577676",
        "Email": "BILLING@WVFC.NET",
        "lat": "45.35497",
        "lng": "-122.60343",
    }

accuracy_input = [
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "FullName": "Bones, Jerry",
            "NPI": "1134523127",
            "FirstName": "Jerry",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Jerry Bones Emp",
            "ADD1": "472 Kneecap Drive",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "1345837645",
            "Fax": "1039273645",
            "Email": "Bones@wackycracky.net",
            "lat": "45.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "FullName": "Lost, Garry",
            "NPI": "1134523127",
            "FirstName": "Gary",
            "LastName": "Lost",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Ripoff Emporium",
            "ADD1": "398 Cheapskate Lane",
            "ADD2": "",
            "City": "Conman City",
            "State": "LI",
            "Zip": "000000000",
            "Phone": "9873640918",
            "Fax": "1090283647",
            "Email": "Cheat@hotmail.com",
            "lat": "84.2313",
            "lng": "646.4531",
        },
]


accuracy_output = [
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "Accuracy": 0.22,
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "Accuracy": 0.22,
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "Accuracy": 0.22,
            "FullName": "Bones, Johnny",
            "NPI": "1134523127",
            "FirstName": "Johnny",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Johnny Bones Emporium",
            "ADD1": "676 Femur Lane",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "3239078654",
            "Fax": "1739216345",
            "Email": "Bones@achybreaky.com",
            "lat": "63.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "Accuracy": 0.28,
            "FullName": "Bones, Jerry",
            "NPI": "1134523127",
            "FirstName": "Jerry",
            "LastName": "Bones",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Jerry Bones Emp",
            "ADD1": "472 Kneecap Drive",
            "ADD2": "",
            "City": "Imperium City",
            "State": "OR",
            "Zip": "970454523",
            "Phone": "1345837645",
            "Fax": "1039273645",
            "Email": "Bones@wackycracky.net",
            "lat": "45.35497",
            "lng": "-213.60343",
        },
        {
            "Endpoint": "",
            "DateRetrieved": "2/1/2024",
            "Accuracy": 0.17,
            "FullName": "Lost, Garry",
            "NPI": "1134523127",
            "FirstName": "Gary",
            "LastName": "Lost",
            "Gender": "M",
            "Taxonomy": "103T00000X",
            "GroupName": "Ripoff Emporium",
            "ADD1": "398 Cheapskate Lane",
            "ADD2": "",
            "City": "Conman City",
            "State": "LI",
            "Zip": "000000000",
            "Phone": "9873640918",
            "Fax": "1090283647",
            "Email": "Cheat@hotmail.com",
            "lat": "84.2313",
            "lng": "646.4531",
        }
]

match_input = [
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "63.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Jerry", 'NPI': "1134523127", 'FirstName': "Jerry",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "104T00000X", 'GroupName': "Jerry Bones Emp", 'ADD1': "472 Kneecap Drive", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "1345837645", 'Fax': "1039273645", 'Email': "Bones@wackycracky.net", 'lat': "45.35497", 'lng': "-213.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Lost, Garry", 'NPI': "1134523127", 'FirstName': "Gary",
        'LastName': "Lost", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Ripoff Emporium", 'ADD1': "398 Cheapskate Lane", 'ADD2': "", 'City': "Conman City",
        'State': "LI", 'Zip': "000000000", 'Phone': "9873640918", 'Fax': "1090283647", 'Email': "Cheat@hotmail.com", 'lat': "84.2313", 'lng': "646.4531"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    },
    {
        'Endpoint': "", 'DateRetrieved': "2/1/2024", 'FullName': "Bones, Johnny", 'NPI': "1134523127", 'FirstName': "Johnny",
        'LastName': "Bones", 'Gender': "M", 'Taxonomy': "103T00000X", 'GroupName': "Johnny Bones Emporium", 'ADD1': "676 Femur Lane", 'ADD2': "", 'City': "Imperium City",
        'State': "OR", 'Zip': "970454523", 'Phone': "3239078654", 'Fax': "1739216345", 'Email': "Bones@achybreaky.com", 'lat': "0.35497", 'lng': "-219.60343"
    }
]

match_output = [
    [{
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Bones, Johnny', 'NPI': '1134523127', 'FirstName': 'Johnny', 
        'LastName': 'Bones', 'Gender': 'M', 'Taxonomy': '103T00000X', 'GroupName': 'Johnny Bones Emporium', 'ADD1': '676 Femur Lane', 
        'ADD2': '', 'City': 'Imperium City', 'State': 'OR', 'Zip': '970454523', 'Phone': '3239078654', 'Fax': '1739216345', 'Email': 'Bones@achybreaky.com', 'lat': '63.35497', 'lng': '-213.60343'
    }, 
    {
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Bones, Johnny', 'NPI': '1134523127', 'FirstName': 'Johnny', 'LastName': 'Bones', 'Gender': 'M', 
        'Taxonomy': '103T00000X', 'GroupName': 'Johnny Bones Emporium', 'ADD1': '676 Femur Lane', 'ADD2': '', 'City': 'Imperium City', 
        'State': 'OR', 'Zip': '970454523', 'Phone': '3239078654', 'Fax': '1739216345', 'Email': 'Bones@achybreaky.com', 'lat': '63.35497', 'lng': '-213.60343'
    }, 
    {
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Bones, Johnny', 'NPI': '1134523127', 'FirstName': 'Johnny', 'LastName': 'Bones', 'Gender': 'M', 'Taxonomy': '103T00000X', 
        'GroupName': 'Johnny Bones Emporium', 'ADD1': '676 Femur Lane', 'ADD2': '', 'City': 'Imperium City', 'State': 'OR', 'Zip': '970454523', 'Phone': '3239078654', 'Fax': '1739216345', 
        'Email': 'Bones@achybreaky.com', 'lat': '63.35497', 'lng': '-213.60343'
    }]

    [{
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Bones, Jerry', 'NPI': '1134523127', 'FirstName': 'Jerry', 'LastName': 'Bones', 'Gender': 'M', 'Taxonomy': '104T00000X', 
        'GroupName': 'Jerry Bones Emp', 'ADD1': '472 Kneecap Drive', 'ADD2': '', 'City': 'Imperium City', 'State': 'OR', 'Zip': '970454523', 'Phone': '1345837645', 
        'Fax': '1039273645', 'Email': 'Bones@wackycracky.net', 'lat': '45.35497', 'lng': '-213.60343'
    }]

    [{
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Lost, Garry', 'NPI': '1134523127', 'FirstName': 'Gary', 'LastName': 'Lost', 'Gender': 'M', 
        'Taxonomy': '103T00000X', 'GroupName': 'Ripoff Emporium', 'ADD1': '398 Cheapskate Lane', 'ADD2': '', 'City': 'Conman City', 'State': 'LI', 'Zip': '000000000', 
        'Phone': '9873640918', 'Fax': '1090283647', 'Email': 'Cheat@hotmail.com', 'lat': '84.2313', 'lng': '646.4531'
    }]
    [{
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 'FullName': 'Bones, Johnny', 'NPI': '1134523127', 'FirstName': 'Johnny', 'LastName': 'Bones', 'Gender': 'M', 
        'Taxonomy': '103T00000X', 'GroupName': 'Johnny Bones Emporium', 'ADD1': '676 Femur Lane', 'ADD2': '', 'City': 'Imperium City', 'State': 'OR', 'Zip': '970454523', 
        'Phone': '3239078654', 'Fax': '1739216345', 'Email': 'Bones@achybreaky.com', 'lat': '0.35497', 'lng': '-219.60343'
    }, 
    {
        'Endpoint': '', 'DateRetrieved': '2/1/2024', 
        'FullName': 'Bones, Johnny', 'NPI': '1134523127', 'FirstName': 'Johnny', 'LastName': 'Bones', 'Gender': 'M', 'Taxonomy': '103T00000X', 'GroupName': 'Johnny Bones Emporium', 
        'ADD1': '676 Femur Lane', 'ADD2': '', 'City': 'Imperium City', 'State': 'OR', 'Zip': '970454523', 'Phone': '3239078654', 'Fax': '1739216345', 'Email': 'Bones@achybreaky.com', 
        'lat': '0.35497', 'lng': '-219.60343'
    }]
]
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

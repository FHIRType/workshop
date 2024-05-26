prac_sample_resource = {
    "id": "123456",
    "language": "en-US",
    "meta": {
        "extension": [
            {"url": "http://example.com/prtr/vendor", "valueBoolean": False},
            {"url": "http://example.com/prtr/directory-display", "valueBoolean": True},
        ],
        "lastUpdated": "2021-06-22T11:03:51.000+00:00",
        "profile": [
            "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Practitioner"
        ],
        "source": "ExampleSource",
    },
    "active": True,
    "address": [
        {
            "city": "SAMPLE CITY",
            "country": "USA",
            "district": "SAMPLEDISTRICT",
            "line": ["123 MAIN ST"],
            "postalCode": "12345-6789",
            "state": "EX",
            "text": "123 MAIN ST,SAMPLE CITY,EX,12345-6789",
            "type": "postal",
            "use": "work",
        }
    ],
    "gender": "female",
    "identifier": [
        {
            "assigner": {
                "display": "Organization Example",
                "reference": "Organization/Example",
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
            "value": "1234567890",
        }
    ],
    "name": [
        {"family": "SMITH", "given": ["JANE", "A"], "text": "SMITH, JANE A"}
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
                "display": "Practitioner/123456",
                "reference": "Practitioner/123456",
            },
            "period": {"start": "2000"},
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
                "display": "Practitioner/123456",
                "reference": "Practitioner/123456",
            },
        },
    ],
    "telecom": [
        {"system": "phone", "use": "work", "value": "555-123-4567"},
        {"system": "fax", "use": "work", "value": "555-765-4321"},
        {"system": "email", "use": "work", "value": "contact@example.com"},
    ],
    "resourceType": "Practitioner",
}

prac_sample_output = {
    "ADD1": None,
    "ADD2": None,
    "Accuracy": -1,
    "City": None,
    "DateRetrieved": "stub",
    "Email": None,
    "Endpoint": "Mock",
    "Fax": None,
    "FirstName": "Jane",
    "FullName": "SMITH, JANE A",
    "Gender": "Female",
    "GroupName": None,
    "LastLocationUpdate": None,
    "LastName": "Smith",
    "LastPracRoleUpdate": None,
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "NPI": 1234567890,
    "Phone": None,
    "State": None,
    "Taxonomy": None,
    "Zip": None,
    "lat": None,
    "lng": None,
}

prac_role_sample_resource = {
    "id": "sample-role-id",
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
        "source": "urn:example:source",
        "versionId": "1234567890",
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
                "reference": "Organization/sample-org-1",
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
                                "display": "Other",
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
                "reference": "Organization/sample-org-2",
                "type": "Organization",
            },
        },
        {
            "url": "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/network-reference",
            "valueReference": {
                "reference": "Organization/sample-org-3",
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
                "reference": "Organization/sample-org-4",
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
            "reference": "HealthcareService/sample-service-1",
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
            "value": "1234567890",
        },
        {
            "system": "https://example.com/r4",
            "use": "usual",
            "value": "sample-unique-id",
        },
    ],
    "location": [
        {
            "reference": "Location/sample-location-1",
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
        "reference": "Practitioner/sample-practitioner-1",
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
    "telecom": [{"rank": 1, "system": "phone", "value": "5551234567"}],
    "resourceType": "PractitionerRole",
}

prac_role_sample_output = {
    "ADD1": None,
    "ADD2": None,
    "Accuracy": -1.0,
    "City": None,
    "DateRetrieved": "stub",
    "Email": None,
    "Endpoint": "Mock",
    "Fax": None,
    "FirstName": "Jane",
    "FullName": "SMITH, JANE A",
    "Gender": "Female",
    "GroupName": None,
    "LastLocationUpdate": None,
    "LastName": "Smith",
    "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "NPI": 1234567890,
    "Phone": None,
    "State": None,
    "Taxonomy": "103T00000X",
    "Zip": None,
    "lat": None,
    "lng": None,
}

prac_loc_sample_resource = {
    "id": "sample-location-id",
    "language": "en",
    "meta": {
        "lastUpdated": "2023-09-12T23:46:56.563Z",
        "profile": [
            "http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/plannet-Location"
        ],
        "source": "urn:example:source",
        "versionId": "1234567890",
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
        "city": "SAMPLE CITY",
        "country": "UNITED STATES",
        "district": "SAMPLEDISTRICT",
        "line": ["123 MAIN ST"],
        "postalCode": "12345-6789",
        "state": "EX",
    },
    "identifier": [
        {
            "value": "1234567890123 MAIN STSAMPLE CITYSAMPLEDISTRICTEX123456789UNITED STATES"
        },
        {
            "system": "https://example.com/r4",
            "use": "usual",
            "value": "sample-unique-id",
        },
    ],
    "name": "123 MAIN ST-12345",
    "position": {"latitude": 10.01, "longitude": -10.01},
    "status": "active",
    "telecom": [{"system": "phone", "use": "work", "value": "5551234567"}],
    "resourceType": "Location",
}

prac_loc_sample_output = {
    "ADD1": "123 MAIN ST",
    "ADD2": None,
    "Accuracy": -1.0,
    "City": "SAMPLE CITY",
    "DateRetrieved": "stub",
    "Email": None,
    "Endpoint": "Mock",
    "Fax": None,
    "FirstName": "Jane",
    "FullName": "SMITH, JANE A",
    "Gender": "Female",
    "GroupName": None,
    "LastLocationUpdate": "2023-09-12T23:46:56Z",
    "LastName": "Smith",
    "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "NPI": 1234567890,
    "Phone": 5551234567,
    "State": "EX",
    "Taxonomy": "103T00000X",
    "Zip": "12345-6789",
    "lat": 10.01,
    "lng": -10.01,
}

prac_all_prac_res_sample_output = {
    "ADD1": "123 MAIN ST",
    "ADD2": None,
    "Accuracy": -1.0,
    "City": "SAMPLE CITY",
    "DateRetrieved": "stub",
    "Email": None,
    "Endpoint": "Mock",
    "Fax": None,
    "FirstName": "Jane",
    "FullName": "SMITH, JANE A",
    "Gender": "Female",
    "GroupName": None,
    "LastLocationUpdate": "2023-09-12T23:46:56Z",
    "LastName": "Smith",
    "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
    "LastPracUpdate": "2021-06-22T11:03:51Z",
    "NPI": 1234567890,
    "Phone": 5551234567,
    "State": "EX",
    "Taxonomy": "103T00000X",
    "Zip": "12345-6789",
    "lat": 10.01,
    "lng": -10.01,
}

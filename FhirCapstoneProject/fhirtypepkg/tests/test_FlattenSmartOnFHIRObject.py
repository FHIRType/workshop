from datetime import datetime
from FhirCapstoneProject.fhirtypepkg.flatten import FlattenSmartOnFHIRObject
from fhirclient.models.practitionerrole import PractitionerRole


def test_constructor_works_as_intended():
    # Arrange
    test_endpoint = "FAKE ENDPOINT"

    # Act
    flatten_smart = FlattenSmartOnFHIRObject(test_endpoint)

    # Assert
    assert flatten_smart.endpoint == test_endpoint
    assert flatten_smart.date_retrieved.replace(
        microsecond=0
    ) == datetime.utcnow().replace(microsecond=0)


def test_flattens_practitioner_as_intended():
    pass


def test_flattens_practitioner_role_as_intended():
    # Arrange
    test_endpoint = "FAKE ENDPOINT"
    test_date = datetime.utcnow()
    fake_resource = {
        "id": "dir-adsgasdbadsgadsf",
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

    # Create an instance of PractitionerRole
    practitioner_role = PractitionerRole()

    # Update the practitioner_role instance with the dictionary
    practitioner_role.update_with_json(fake_resource)

    fake_flatten = [
        {
            "Endpoint": test_endpoint,
            "DateRetrieved": test_date,
            "FullName": "Invalid attribute key",
            "NPI": "1013072586",
            "FirstName": "Invalid attribute key",
            "LastName": "Invalid attribute key",
            "Gender": "Invalid attribute key",
            "Taxonomy": "Invalid attribute key",
            "GroupName": "GroupName_data",
            "ADD1": "Invalid attribute key",
            "ADD2": None,
            "City": "Invalid attribute key",
            "State": "Invalid attribute key",
            "Zip": "Invalid attribute key",
            "Phone": "5036577235",
            "Fax": None,
            "Email": None,
            "lat": None,
            "lng": None,
            "LastPracUpdate": None,
            "LastPracRoleUpdate": "2023-11-09T03:23:38Z",
            "LastLocationUpdate": None,
            "AccuracyScore": None,
        }
    ]

    # Act
    flatten_smart = FlattenSmartOnFHIRObject(test_endpoint)
    flatten_smart.flatten_practitioner_role_object(practitioner_role)

    # Round the test_date in fake_flatten
    fake_flatten[0]["DateRetrieved"] = str(test_date).split(".")[0]

    # Round the Date Retrieved in flatten_smart.prac_role_obj
    flatten_smart.prac_role_obj[0]["DateRetrieved"] = str(
        flatten_smart.prac_role_obj[0]["DateRetrieved"]
    ).split(".")[0]

    # Print both for debugging
    print("Expected:", fake_flatten)
    print("Actual:", flatten_smart.prac_role_obj)

    # Assert
    assert flatten_smart.prac_role_obj == fake_flatten

from FhirCapstoneProject.fhirtypepkg.flatten import FlattenSmartOnFHIRObject
from FhirCapstoneProject.tests.assets.prac_resource_sample import (
    prac_sample_output,
    prac_sample_resource,
    prac_role_sample_resource,
    prac_role_sample_output,
    prac_loc_sample_output,
    prac_loc_sample_resource,
    prac_all_prac_res_sample_output
)

from fhirclient.models.location import Location
from fhirclient.models.practitionerrole import PractitionerRole
from fhirclient.models.practitioner import Practitioner


def test_flatten_smart_on_fhir_object_initialization():
    # Arrange
    test_endpoint = "FAKE ENDPOINT"

    # Act
    flatten_smart = FlattenSmartOnFHIRObject(test_endpoint)

    # Assert
    assert flatten_smart.metadata["Endpoint"] == test_endpoint
    assert isinstance(flatten_smart.metadata["DateRetrieved"], str)
    assert flatten_smart.metadata["Accuracy"] == -1.0


def test_flatten_all_with_prac_obj_only():
    # Arrange
    test_endpoint = "Centene"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)

    # Act
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_flattened_data()
    expected_data = [prac_sample_output]

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    for data in flatten_data:
        data.pop("DateRetrieved", None)
    expected_data[0].pop("DateRetrieved", None)

    assert flatten_data == expected_data


def test_flatten_all_with_prac_role_obj_only():
    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Act
    flatten_smart.flatten_all()

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_related_flat_data()
    expected_data = [prac_role_sample_output]

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    for data in flatten_data:
        data.pop("DateRetrieved", None)
    expected_data[0].pop("DateRetrieved", None)

    assert flatten_data == expected_data


def test_flatten_all_with_prac_loc_obj_only():
    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Act
    flatten_smart.flatten_all()

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)

    # Act
    flatten_smart.flatten_all()

    # Arrange
    practitioner_location = Location()
    practitioner_location.update_with_json(prac_loc_sample_resource)
    flatten_smart.prac_loc_obj.append(practitioner_location)

    # Act
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_related_flat_data()
    expected_data = [prac_loc_sample_output]

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    for data in flatten_data:
        data.pop("DateRetrieved", None)
    expected_data[0].pop("DateRetrieved", None)

    assert flatten_data == expected_data


def test_flatten_all_with_all_resource_data():
    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Act
    flatten_smart.flatten_all()

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)

    # Act
    flatten_smart.flatten_all()

    # Arrange
    practitioner_location = Location()
    practitioner_location.update_with_json(prac_loc_sample_resource)
    flatten_smart.prac_loc_obj.append(practitioner_location)

    # Act
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_flattened_data()
    expected_data = [prac_all_prac_res_sample_output]

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    for data in flatten_data:
        data.pop("DateRetrieved", None)
    expected_data[0].pop("DateRetrieved", None)

    assert flatten_data == expected_data

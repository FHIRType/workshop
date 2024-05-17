from FhirCapstoneProject.fhirtypepkg.flatten import FlattenSmartOnFHIRObject
from FhirCapstoneProject.tests.assets.prac_resource_sample import (
    prac_sample_output,
    prac_sample_resource,
    prac_role_sample_resource,
    prac_role_sample_output,
    prac_loc_sample_output,
    prac_loc_sample_resource,
    prac_all_prac_res_sample_output,
)

from fhirclient.models.location import Location
from fhirclient.models.practitionerrole import PractitionerRole
from fhirclient.models.practitioner import Practitioner


def test_flatten_smart_on_fhir_object_initialization():
    """
    Test initialization of FlattenSmartOnFHIRObject.

    Asserts that the metadata and its initial values are correctly set upon object initialization.
    """
    # Arrange
    test_endpoint = "FAKE ENDPOINT"

    # Act
    flatten_smart = FlattenSmartOnFHIRObject(test_endpoint)

    # Assert
    assert flatten_smart.metadata["Endpoint"] == test_endpoint
    assert isinstance(flatten_smart.metadata["DateRetrieved"], str)
    assert flatten_smart.metadata["Accuracy"] == -1.0


def test_flatten_all_with_prac_obj_only():
    """
    Test flattening when only Practitioner object is present.

    Asserts that flattening a Practitioner object results in the expected flattened data.
    """
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
    expected_data = prac_sample_output

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    flatten_data["DateRetrieved"] = "stub"

    assert flatten_data == expected_data


def test_flatten_all_with_prac_role_obj_only():
    """
    Test flattening when only PractitionerRole object is present.

    Asserts that flattening a PractitionerRole object results in the expected flattened data.
    """
    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_flattened_data()
    expected_data = prac_role_sample_output

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    flatten_data["DateRetrieved"] = "stub"

    assert flatten_data == expected_data


def test_flatten_all_with_prac_loc_obj_only():
    """
    Test flattening when only Location object is present.

    Asserts that flattening a Location object results in the expected flattened data.
    """
    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)

    # Arrange
    practitioner_location = Location()
    practitioner_location.update_with_json(prac_loc_sample_resource)
    flatten_smart.prac_loc_obj.append(practitioner_location)

    # Act
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_flattened_data()
    expected_data = prac_loc_sample_output

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    flatten_data["DateRetrieved"] = "stub"

    assert flatten_data == expected_data


def test_flatten_all_with_all_resource_data():
    """
    Test flattening when all resource data is present.

    Asserts that flattening all available resource data results in the expected flattened data.
    """

    # Arrange
    test_endpoint = "Cigna"
    flatten_smart = FlattenSmartOnFHIRObject(endpoint=test_endpoint)
    practitioner = Practitioner()
    practitioner.update_with_json(prac_sample_resource)
    flatten_smart.prac_obj = practitioner  # Mock practitioner object

    # Arrange
    practitioner_role = PractitionerRole()
    practitioner_role.update_with_json(prac_role_sample_resource)
    flatten_smart.prac_role_obj.append(practitioner_role)

    # Arrange
    practitioner_location = Location()
    practitioner_location.update_with_json(prac_loc_sample_resource)
    flatten_smart.prac_loc_obj.append(practitioner_location)

    # Act
    flatten_smart.flatten_all()

    # Assert
    flatten_data = flatten_smart.get_flattened_data()
    expected_data = prac_all_prac_res_sample_output

    # Directly remove 'DateRetrieved' from the actual and expected data dictionaries
    flatten_data["DateRetrieved"] = "stub"

    assert flatten_data == expected_data

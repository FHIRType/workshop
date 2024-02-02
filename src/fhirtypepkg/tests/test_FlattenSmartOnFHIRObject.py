from datetime import datetime
from fhirtypepkg.flatten import FlattenSmartOnFHIRObject


def test_constructor_works_as_intended():
    # Arrange
    test_date = datetime.utcnow()
    test_endpoint = "FAKE ENDPOINT"

    # Act
    flatten_smart = FlattenSmartOnFHIRObject(test_endpoint)

    # Assert
    assert flatten_smart.endpoint == test_endpoint
    assert flatten_smart.date_retrieved.replace(microsecond=0) == datetime.utcnow().replace(microsecond=0)

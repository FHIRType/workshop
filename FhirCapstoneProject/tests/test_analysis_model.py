# Authors: Iain Richey
# Description: Tests the analysis model
from FhirCapstoneProject.model.analysis import predict
from FhirCapstoneProject.tests.assets.mock_models_samples import (
    analysis_output,
    analysis_test_input,
)


def test_analysis_model():
    """
    Tests that queries the analysis model
    :return:
    """
    consensus = predict(analysis_test_input)

    print(consensus)

    assert consensus == analysis_output

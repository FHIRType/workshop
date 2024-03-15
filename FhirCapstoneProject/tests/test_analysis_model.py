# Authors: Iain Richey
# Description: Tests the analysis model
from FhirCapstoneProject.model.analysis import predict
from FhirCapstoneProject.tests.assets.prac_resource_sample import (
    analysis_output,
    analysis_test_input
)

def test_analysis_model():
    consensus = predict(analysis_test_input)

    print(consensus)

    assert consensus == analysis_output
# Authors: Iain Richey
# Description: Tests the analysis model
from FhirCapstoneProject.fhirtypepkg.analysis import predict
import pytest
from json import loads
from deepdiff import DeepDiff
from FhirCapstoneProject.tests.assets.prac_resource_sample import (
    analysis_output,
    analysis_test_input
)

def test_analysis_model():
    consensus = predict(analysis_test_input)

    print(consensus)
    print(analysis_output)

    diff = DeepDiff(consensus, analysis_output)

    assert not diff
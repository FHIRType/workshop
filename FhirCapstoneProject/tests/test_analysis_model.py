# Authors: Iain Richey
# Description: Tests the analysis model
from FhirCapstoneProject.fhirtypepkg.analysis import predict
import pytest
from json import loads
from deepdiff import DeepDiff

def test_analysis_model(expected_input, analysis_prediction):
    return 0
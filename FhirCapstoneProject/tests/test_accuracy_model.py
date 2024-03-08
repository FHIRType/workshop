# Authors: Iain Richey
# Description: Tests the accuracy model
from FhirCapstoneProject.model.accuracy import calc_accuracy
import pytest
from json import loads, dumps
from deepdiff import DeepDiff
from FhirCapstoneProject.tests.assets.prac_resource_sample import (
    accuracy_input,
    accuracy_output,
    accuracy_consensus
)

def test_accuracy_model():
    json_string = calc_accuracy(accuracy_input, accuracy_consensus)
    output_dict = loads(dumps(json_string))

    assert output_dict == accuracy_output

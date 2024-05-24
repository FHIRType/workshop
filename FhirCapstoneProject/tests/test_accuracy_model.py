# Authors: Iain Richey
# Description: Tests the accuracy model
from FhirCapstoneProject.model.accuracy import calc_accuracy
import pytest
from json import loads, dumps
from FhirCapstoneProject.tests.assets.mock_accuracy_samples import (
    accuracy_input,
    accuracy_output,
    accuracy_consensus,
)


def test_accuracy_model():
    json_string = calc_accuracy(accuracy_input, accuracy_consensus)
    output_dict = loads(dumps(json_string))

    for index in range(len(output_dict)):
        assert output_dict[index] == accuracy_output[index]

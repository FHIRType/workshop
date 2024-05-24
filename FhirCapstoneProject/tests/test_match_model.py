# Authors: Iain Richey
# Description: Tests the accuracy model
from FhirCapstoneProject.model.match import group_rec
import pytest
from json import loads, dumps
from FhirCapstoneProject.tests.assets.mock_accuracy_samples import (
    match_input,
    match_output,
)


def test_match_model():
    json_string = group_rec(match_input, False)
    output_dict = loads(dumps(json_string))

    # print (output_dict)

    assert output_dict == match_output

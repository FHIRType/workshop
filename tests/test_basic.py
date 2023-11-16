# Authors: Iain Richey, Trenton Young
# Description: Tests the connection to an arbitrary endpoint in the current configuration.
import random

import pytest
import configparser
from fhirtypepkg.endpoint import Endpoint
from fhirtypepkg.client import SmartClient
from fhirtypepkg.standardize import getKaiserData, getHumanaData


reader = configparser.ConfigParser()
reader.read_file(open('src/fhirtypepkg/config/Endpoints.ini', 'r'))
sections = reader.sections()

choice = random.choice(sections)

endpoint = Endpoint(reader.get(choice, "name"), reader.get(choice, "host"), reader.get(choice, "address"), reader.getboolean(choice, "ssl"))


# def f():
#     raise SystemExit(1)


def test_mytest():
    client = SmartClient(endpoint)
    # with pytest.raises(SystemExit):
    #     f()
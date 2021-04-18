from pathlib import Path

import pytest

from correction import Marker

PWD = Path(__file__).parent.absolute()

ASGMT_FILE = PWD / 'asgmt.py'
CONFIG_FILE = PWD / 'config.yml'
ASGMT_ID = 'basic'


@pytest.fixture
def marker():
    m = Marker(ASGMT_FILE, CONFIG_FILE, ASGMT_ID)
    yield m
    m.injected_asgmt_file.unlink()


@pytest.fixture
def config_file():
    return CONFIG_FILE


@pytest.fixture
def asgmt_file():
    return ASGMT_FILE

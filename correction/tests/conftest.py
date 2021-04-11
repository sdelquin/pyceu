from pathlib import Path

import pytest
import services

PWD = Path(__file__).parent.absolute()

ASGMT_FILE = PWD / 'asgmt.py'
CONFIG_FILE = PWD / 'config.yml'
ASGMT_ID = 'basic'


@pytest.fixture
def asgmt_file():
    return ASGMT_FILE


@pytest.fixture
def config_file():
    return CONFIG_FILE


@pytest.fixture
def testbench():
    return services.read_config(CONFIG_FILE, ['testbench', ASGMT_ID])

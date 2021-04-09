import re
from pathlib import Path

import check
import pytest
import services

PWD = Path(__file__).parent.absolute()

ASGMT_FILEPATH = 'testbench/asgmt.py'
TESTBENCH_FILEPATH = 'testbench/config.yml'
ASGMT_ID = 'basic'


@pytest.fixture
def asgmt_file():
    return PWD / ASGMT_FILEPATH


@pytest.fixture
def testbench():
    f = PWD / TESTBENCH_FILEPATH
    return services.read_testbench(f)


def test_securized_code(asgmt_file):
    securized_asgmt_file = check.create_securized_asgmt_file(asgmt_file)
    assert isinstance(securized_asgmt_file, Path)
    securized_code = securized_asgmt_file.read_text()
    assert re.findall(r'^[^#\n]*\bimport\b.*$', securized_code, re.MULTILINE) == []
    securized_asgmt_file.unlink()


def test_injected_code(asgmt_file, testbench):
    testbench = testbench.get(ASGMT_ID)
    injected_asgmt_file = check.create_injected_asgmt_file(asgmt_file, testbench)
    assert isinstance(injected_asgmt_file, Path)
    injected_code = injected_asgmt_file.read_text()
    assert re.search(r'^import sys', injected_code) is not None
    assert re.search(r'print\(globals.*\)$', injected_code) is not None
    injected_asgmt_file.unlink()


def test_run(asgmt_file, testbench):
    testbench = testbench.get(ASGMT_ID)
    injected_asgmt_file = check.create_injected_asgmt_file(asgmt_file, testbench)
    for case in testbench['cases']:
        code_works = check.handle_testbench_case(case, injected_asgmt_file)
        assert code_works is True
    injected_asgmt_file.unlink()

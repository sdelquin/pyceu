import re
from pathlib import Path

import check


def test_securized_code(asgmt_file):
    securized_asgmt_file = check.create_securized_asgmt_file(asgmt_file)
    assert isinstance(securized_asgmt_file, Path)
    securized_code = securized_asgmt_file.read_text()
    assert re.findall(r'^[^#\n]*\bimport\b.*$', securized_code, re.MULTILINE) == []
    securized_asgmt_file.unlink()


def test_injected_code(asgmt_file, testbench):
    injected_asgmt_file = check.create_injected_asgmt_file(asgmt_file, testbench)
    assert isinstance(injected_asgmt_file, Path)
    injected_code = injected_asgmt_file.read_text()
    assert re.search(r'^import sys', injected_code) is not None
    assert re.search(r'print\(globals.*\)$', injected_code) is not None
    injected_asgmt_file.unlink()


def test_run(asgmt_file, testbench):
    injected_asgmt_file = check.create_injected_asgmt_file(asgmt_file, testbench)
    for case in testbench['cases']:
        code_works, exception_raised = check.handle_testbench_case(
            case, injected_asgmt_file
        )
        assert code_works is True
        assert exception_raised is False
    injected_asgmt_file.unlink()


def test_get_runtime_feedback(asgmt_file, testbench, config_file):
    feedback = testbench.get('feedback', {})
    user_feedback = check.get_runtime_feedback(asgmt_file, feedback)
    assert user_feedback[0]['regex'] == 'for'

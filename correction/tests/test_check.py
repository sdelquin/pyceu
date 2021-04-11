import re
from pathlib import Path

import check
import services


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
        code_works = check.handle_testbench_case(case, injected_asgmt_file)
        assert code_works is True
    injected_asgmt_file.unlink()


def test_contrib_feedback(asgmt_file, testbench, config_file):
    global_feedback = services.read_config(config_file, ['global', 'feedback'])
    asgmt_feedback = testbench.get('feedback', {})
    feedback = services.merge_feedbacks(asgmt_feedback, global_feedback)
    user_feedback = check.contrib_feedback(asgmt_file, feedback)
    assert user_feedback[0]['regex'] == 'for'
    assert user_feedback[1]['linenos'] == [6]

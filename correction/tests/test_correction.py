import re
from pathlib import Path


def test_securized_code(marker):
    securized_asgmt_file = marker.create_securized_asgmt_file()
    assert isinstance(securized_asgmt_file, Path)
    securized_code = securized_asgmt_file.read_text()
    assert re.findall(r'^[^#\n]*\bimport\b.*$', securized_code, re.MULTILINE) == []


def test_injected_code(marker):
    injected_asgmt_file = marker.create_injected_asgmt_file()
    assert isinstance(injected_asgmt_file, Path)
    injected_code = injected_asgmt_file.read_text()
    assert re.search(r'^import sys', injected_code) is not None
    assert re.search(r'print\(globals.*\)$', injected_code) is not None


def test_run(marker):
    for testcase in marker.testbench_cfg['cases']:
        code_works, exception_raised = marker.handle_testbench_case(testcase)
        assert code_works is True
        assert exception_raised is False


def test_get_runtime_feedback(marker):
    feedback = marker.get_runtime_feedback()
    assert feedback[0]['regex'] == 'for'


def test_get_style_feedback(marker):
    feedback = marker.get_style_feedback()
    assert "F401 'os' imported but unused" in feedback
    assert "F401 'sys.argv' imported but unused" in feedback
    assert "E211 whitespace before '('" in feedback

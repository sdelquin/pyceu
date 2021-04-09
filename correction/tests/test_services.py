import re
from pathlib import Path

import services

PWD = Path(__file__).parent.absolute()

TESTBENCH_FILEPATH = 'testbench/config.yml'


def test_parse_exception():
    exception = '''Traceback (most recent call last):
  File "<string>", line 1, in <module>
ZeroDivisionError: division by zero'''
    exception_summary = services.parse_exception(exception)
    assert re.search(r'\w+Error', exception_summary) is not None
    assert re.search(r'line \d+', exception_summary) is not None


def test_read_testbench():
    testbench = services.read_testbench(PWD / TESTBENCH_FILEPATH)
    assert isinstance(testbench, dict)
    assert 'basic' in testbench


def test_list_asgmts(capsys):
    testbench = services.read_testbench(PWD / TESTBENCH_FILEPATH)
    services.show_testbench(testbench)
    captured = capsys.readouterr()
    assert 'basic' in captured.out
    assert 'Basic Test Bench' in captured.out

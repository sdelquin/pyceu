import os
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


def test_clean_files():
    dummy_filename = 'dummy.file'
    dummy_file = Path(dummy_filename)
    dummy_file.write_text('Just dummy!')
    services.clean_files(dummy_file)
    assert os.path.isfile(dummy_filename) is False


def test_show_code(capsys):
    services.show_code(Path(__file__))
    captured = capsys.readouterr()
    assert 'def test_show_code(capsys):' in captured.out


def test_benchtest_results(capsys):
    benchtest_results = [True, False, True]
    correction_display = (
        ('red', '❌', 'NO APTO', '🙁'),
        ('green', '✅', 'APTO', '🥳'),
    )
    services.show_benchtest_results(benchtest_results, correction_display)
    captured = capsys.readouterr()
    assert 'NO APTO' in captured.out

import os
import re
from pathlib import Path

import services


def test_parse_exception():
    exception = '''Traceback (most recent call last):
  File "<string>", line 1, in <module>
ZeroDivisionError: division by zero'''
    exception_summary = services.parse_exception(exception)
    assert re.search(r'\w+Error', exception_summary) is not None
    assert re.search(r'line \d+', exception_summary) is not None


def test_read_config(config_file):
    config = services.read_config(config_file)
    assert isinstance(config, dict)
    assert config['testbench']['basic']['title'] == 'Basic Test Bench'


def test_list_asgmts(config_file, capsys):
    testbench = services.read_config(config_file, ['testbench'])
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


def test_show_testbench_results(capsys):
    testbench_results = [True, False, True]
    correction_display = (
        ('red', '❌', 'NO APTO', '🙁'),
        ('green', '✅', 'APTO', '🥳'),
    )
    services.show_testbench_results(testbench_results, correction_display)
    captured = capsys.readouterr()
    assert 'NO APTO' in captured.out


def test_prepare_runtime_feedback():
    user_feedback = [
        {'regex': 'foo', 'message': 'bar'},
        {'regex': 'baa', 'message': 'bum'},
    ]
    display_items = services.prepare_runtime_feedback(user_feedback)
    assert 'bar' in display_items
    assert 'bum' in display_items


def test_prepare_style_feedback():
    style_feedback = """tests/asgmt.py:1:1: F401 'os' imported but unused
tests/asgmt.py:2:1: F401 'sys.argv' imported but unused
tests/asgmt.py:6:10: E211 whitespace before '('"""
    display_items = services.prepare_style_feedback(style_feedback)
    assert len(display_items.split('\n')) == 4  # 3 + heading
    assert 'L1' in display_items
    assert 'L2' in display_items
    assert 'L6' in display_items
    assert "'os' imported but unused" in display_items.lower()
    assert "'sys.argv' imported but unused" in display_items.lower()
    assert "whitespace before '('" in display_items.lower()


def test_prepare_lang_feedback():
    lang_feedback = 'whatelse'
    display_items = services.prepare_lang_feedback(lang_feedback)
    assert len(display_items.split('\n')) == 2  # 1 + heading
    assert lang_feedback in display_items

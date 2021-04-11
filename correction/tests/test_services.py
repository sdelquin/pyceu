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


def test_merge_feedbacks():
    f1 = {'a': [1, 2], 'b': [3, 4]}
    f2 = {'b': [5, 6], 'c': [7, 8]}
    f = services.merge_feedbacks_cfg(f1, f2)
    assert f['a'] == [1, 2]
    assert f['b'] == [3, 4, 5, 6]
    assert f['c'] == [7, 8]


def test_prepare_user_feedback():
    user_feedback = [
        {'regex': 'foo', 'message': 'bar'},
        {'regex': 'baa', 'message': 'bum', 'linenos': [1, 2, 3]},
    ]
    display_items = services.prepare_user_feedback(user_feedback)
    assert 'bar' in display_items
    assert 'bum' in display_items
    assert 'L1' in display_items
    assert 'L2' in display_items
    assert 'L3' in display_items

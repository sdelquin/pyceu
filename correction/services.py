import re
from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

console = Console()


def parse_exception(exception_message):
    if m := re.search(r'\w+Error:.*', exception_message):
        exception_type = m.group()
        if m := re.search(r'line \d+', exception_message):
            exception_at = m.group()
            exception_summary = f'{exception_type} ({exception_at})'
        else:
            exception_summary = exception_type
    else:
        exception_summary = 'Exception'
    return exception_summary


def show_error(msg: str):
    console.print(f'[orange_red1]⚠️  {msg}')


def read_testbench(testbench_path: str, asgmt_id: str = None):
    testbench = Path(testbench_path)
    payload = yaml.load(testbench.read_text(), Loader=yaml.FullLoader)
    if asgmt_id is not None:
        payload = payload[asgmt_id]
    return payload


def show_testbench(testbench: dict):
    table = Table(title='Available assignments')
    table.add_column("id", justify="right", style="cyan", no_wrap=True)
    table.add_column("title", justify="left", style="magenta", no_wrap=True)
    for asgmt_id, data in testbench.items():
        table.add_row(asgmt_id, data['title'])
    console.print(table)

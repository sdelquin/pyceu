import re
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
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
    console.print(f'[red1]❌️  {msg}')


def read_config(config_path: str, key: list[str] = []):
    config = Path(config_path)
    payload = yaml.load(config.read_text(), Loader=yaml.FullLoader)
    for k in key:
        payload = payload.get(k, {})
    return payload


def show_testbench(testbench: dict):
    table = Table(title='Available assignments')
    table.add_column("id", justify="right", style="cyan", no_wrap=True)
    table.add_column("title", justify="left", style="magenta", no_wrap=True)
    for asgmt_id, data in testbench.items():
        table.add_row(asgmt_id, data['title'])
    console.print(table)


def clean_files(*files: list[Path]):
    for file in files:
        file.unlink()


def show_code(file: Path, language='python', line_numbers=True):
    console.print(f'[bold green_yellow]>> {file.name}')
    syntax = Syntax(
        file.read_text(),
        language,
        line_numbers=line_numbers,
    )
    console.print(syntax)


def show_benchtest_results(benchtest_results: list[bool], correction_display: tuple):
    all_passed = all(benchtest_results)
    color, _, mark, symbol = correction_display[all_passed]
    msg = f'{mark} ({sum(benchtest_results)}/{len(benchtest_results)}) {symbol}'
    panel = Panel(msg, expand=False, style=color)
    console.print(panel)


def merge_feedbacks(feedback1: dict, feedback2: dict):
    feedback = feedback1 | feedback2
    for key in feedback:
        feedback[key] = feedback1.get(key, []) + feedback2.get(key, [])
    return feedback

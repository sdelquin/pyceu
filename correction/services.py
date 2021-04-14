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


def list_asgmts(config_path: str):
    config_file = Path(config_path)
    config = yaml.load(config_file.read_text(), Loader=yaml.FullLoader)
    testbench = config['testbench']
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


def show_testbench_results(testbench_results: list[bool], correction_display: tuple):
    all_passed = all(testbench_results)
    color, _, mark, symbol = correction_display[all_passed]
    msg = f'{mark} ({sum(testbench_results)}/{len(testbench_results)}) {symbol}'
    panel = Panel(msg, expand=False, style=color)
    console.print(panel)


def prepare_runtime_feedback(user_feedback: list[dict]):
    buffer, header = list(), 'Runtime Feedback:'
    for item in user_feedback:
        message = f'- {item["message"]}'
        buffer.append(message)
    if buffer:
        buffer.insert(0, header)
    return '\n'.join(buffer)


def prepare_style_feedback(style_feedback: str):
    buffer, header = list(), 'Style Feedback (flake8):'
    for line in style_feedback.strip().split('\n'):
        if s := re.search(r'(\d+):\d+: [FEW]\d+ (.*)$', line):
            lineno, msg = s.groups()
            message = f'- {msg.capitalize()} (L{lineno})'
            buffer.append(message)
    if buffer:
        buffer.insert(0, header)
    return '\n'.join(buffer)


def prepare_lang_feedback(lang_feedback: str):
    buffer, header = list(), 'Language Feedback:'
    buffer.append(f'- {lang_feedback}')
    if buffer:
        buffer.insert(0, header)
    return '\n'.join(buffer)


def securize_code(code: str):
    securized_code = []
    for line in code.split('\n'):
        if re.search(r'\bimport\b', line):
            securized_line = '# ' + line
        else:
            securized_line = line
        securized_code.append(securized_line)
    return '\n'.join(securized_code)


def inject_checking_code(code: str, input_vars: list[str], output_vars: list[str]):
    # imports
    code = 'import sys\n\n' + code
    # initial values for input variables
    for i, var in enumerate(input_vars):
        if isinstance(var, dict):
            # typecast is set
            varname, cast = tuple(var.items())[0]
        else:
            varname, cast = var, 'str'
        code = re.sub(
            rf'{varname} *=.*', f'{varname} = {cast}(sys.argv[{i + 1}])', code, count=1
        )
    # print statements for output variables
    print_statements = []
    for varname in output_vars:
        print_statements.append(f"print(globals().get('{varname}', 'UNDEF'), end=' ')")
    print_statements = '\n'.join(print_statements)

    code = code + '\n' + print_statements + '\n'
    return code

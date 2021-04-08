import re
import subprocess
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

CORRECTION_DISPLAY = (
    ('red', '❌', 'NO APTO', '🙁'),
    ('green', '✅', 'APTO', '🥳'),
)


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


def run_test(filename, args, desired_output):
    command = f'python "{filename}" {args}'
    console.print(f'[bold cyan]$ {command}')
    try:
        output = subprocess.check_output(
            command, encoding='utf-8', shell=True, stderr=subprocess.STDOUT
        )
    except Exception as err:
        output = parse_exception(err.output)
    else:
        output = output.strip().split('\n')[-1]
    code_works = output == desired_output
    return output, code_works


def inject_checking_code(code, input_vars, output_vars):
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


def create_injected_asgmt_file(asgmt_file: Path, config: list):
    asgmt_code = asgmt_file.read_text()
    injected_asgmt_code = inject_checking_code(
        asgmt_code, config['vars']['input'], config['vars']['output']
    )
    injected_asgmt_filename = asgmt_file.stem + '.injected' + asgmt_file.suffix
    injected_asgmt_file = Path(injected_asgmt_filename)
    injected_asgmt_file.write_text(injected_asgmt_code)
    return injected_asgmt_file


def securize_code(asgmt_file: Path):
    asgmt_code = asgmt_file.read_text()
    securized_code = []
    for line in asgmt_code.split('\n'):
        if re.search(r'\bimport\b', line):
            securized_line = '#' + line
        else:
            securized_line = line
        securized_code.append(securized_line)
    asgmt_file.write_text('\n'.join(securized_code))


def handle_assignment(asgmt_id: str, asgmt_file: Path, clean_files):
    markdown = Markdown(f'# {asgmt_file.name}')
    console.print(markdown)

    securize_code(asgmt_file)

    passed = []
    config = yaml.load(Path('config.yml').read_text(), Loader=yaml.FullLoader)[asgmt_id]
    injected_asgmt_file = create_injected_asgmt_file(asgmt_file, config)

    for case in config['cases']:
        args = ' '.join(str(v) for v in case['input'])
        desired_output = ' '.join(str(v) for v in case['output'])
        output, code_works = run_test(injected_asgmt_file.name, args, desired_output)
        print('Desired output:', desired_output)
        color, symbol = CORRECTION_DISPLAY[code_works][:2]
        console.print(f'[{color}]Program output: {output} {symbol}')
        passed.append(code_works)

    all_passed = all(passed)
    color, _, mark, symbol = CORRECTION_DISPLAY[all_passed]
    msg = f'{mark} ({sum(passed)}/{len(passed)}) {symbol}'
    panel = Panel(msg, expand=False, style=color)
    console.print(panel)

    if not all_passed:
        syntax = Syntax(
            injected_asgmt_file.read_text(),
            'python',
            line_numbers=True,
        )
        console.print(syntax)

    if clean_files:
        asgmt_file.unlink()
        injected_asgmt_file.unlink()


def main(
    asgmt_id: str = typer.Argument(
        ..., help='Assignment identifier as written in config.yml'
    ),
    asgmt_folder_path: str = typer.Argument(
        ..., help='Path to the folder where assignments are saved (e.g. ~/Downloads)'
    ),
    keep_files: bool = typer.Option(
        False, '-k', help='Do not remove input file (and injected code) after execution'
    ),
):
    asgmt_folder = Path(asgmt_folder_path)
    try:
        # It expects only one .py file to be checked
        asgmt_file = next(asgmt_folder.glob('*.py'))
    except StopIteration:
        console.print(f'[orange_red1]⚠️  No .py files found in {asgmt_folder}')
    else:
        handle_assignment(asgmt_id, asgmt_file, not keep_files)


if __name__ == '__main__':
    # https://bit.ly/3t2hLRx
    app = typer.Typer(add_completion=False)
    app.command()(main)
    app()

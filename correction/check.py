import re
import subprocess
from pathlib import Path

import services
import settings
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def run_test(filename, args, desired_output):
    command = f'python "{filename}" {args}'
    console.print(f'[bold cyan]$ {command}')
    try:
        output = subprocess.check_output(
            command, encoding='utf-8', shell=True, stderr=subprocess.STDOUT
        )
    except Exception as err:
        output = services.parse_exception(err.output)
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
    try:
        config = services.read_testbench()[asgmt_id]
    except KeyError:
        services.show_error(f'Assignment id "{asgmt_id}" not found!')
        return
    injected_asgmt_file = create_injected_asgmt_file(asgmt_file, config)

    for case in config['cases']:
        args = ' '.join(str(v) for v in case['input'])
        desired_output = ' '.join(str(v) for v in case['output'])
        output, code_works = run_test(injected_asgmt_file.name, args, desired_output)
        print('Desired output:', desired_output)
        color, symbol = settings.CORRECTION_DISPLAY[code_works][:2]
        console.print(f'[{color}]Program output: {output} {symbol}')
        passed.append(code_works)

    all_passed = all(passed)
    color, _, mark, symbol = settings.CORRECTION_DISPLAY[all_passed]
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

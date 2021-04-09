import re
import subprocess
from pathlib import Path

import services
import settings
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm
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
    console.print('[magenta]Injecting testing code...')
    asgmt_code = asgmt_file.read_text()
    injected_asgmt_code = inject_checking_code(
        asgmt_code, config['vars']['input'], config['vars']['output']
    )
    injected_asgmt_filename = asgmt_file.stem + '.injected' + asgmt_file.suffix
    injected_asgmt_file = Path(injected_asgmt_filename)
    injected_asgmt_file.write_text(injected_asgmt_code)
    return injected_asgmt_file


def securize_code(code: str):
    securized_code = []
    for line in code.split('\n'):
        if re.search(r'\bimport\b', line):
            securized_line = '#' + line
        else:
            securized_line = line
        securized_code.append(securized_line)
    return '\n'.join(securized_code)


def create_securized_asgmt_file(asgmt_file: Path):
    console.print('[magenta]Securizing input code...')
    asgmt_code = asgmt_file.read_text()
    securized_asgmt_code = securize_code(asgmt_code)
    securized_asgmt_filename = asgmt_file.stem + '.securized' + asgmt_file.suffix
    securized_asgmt_file = Path(securized_asgmt_filename)
    securized_asgmt_file.write_text(securized_asgmt_code)
    return securized_asgmt_file


def handle_assignment(asgmt_file: Path, testbench: list, clean_files: bool = True):
    markdown = Markdown(f'# {asgmt_file.name}')
    console.print(markdown)

    securized_asgmt_file = create_securized_asgmt_file(asgmt_file)
    injected_asgmt_file = create_injected_asgmt_file(securized_asgmt_file, testbench)

    passed = []
    for case in testbench['cases']:
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

    view_code = Confirm.ask('Do you want to see the code?', default=not all_passed)
    if view_code:
        file_to_show = asgmt_file if all_passed else injected_asgmt_file
        console.print(f'[bold green_yellow]>> {file_to_show.name}')
        syntax = Syntax(
            file_to_show.read_text(),
            'python',
            line_numbers=True,
        )
        console.print(syntax)

    if clean_files:
        console.print('[magenta]Cleaning temp files and assignment code...')
        asgmt_file.unlink()
        securized_asgmt_file.unlink()
        injected_asgmt_file.unlink()

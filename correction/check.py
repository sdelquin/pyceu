import re
import subprocess
import sys
from pathlib import Path

import yaml
from rich.console import Console

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
    console.print(f'[dark_goldenrod]$ {command}')
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


def handle_assignment(asgmt_id: str, asgmt_file: Path):
    console.print(f'[white bold]Checking "{asgmt_file.name}"\n')

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
    print('-------------------------------------')
    console.print(f'[{color}]{mark} ({sum(passed)}/{len(passed)}) {symbol}')

    if not all_passed:
        console.print(f'[dark_goldenrod]{injected_asgmt_file}\n\n')
        console.print(injected_asgmt_file.read_text())

    # asgmt_file.unlink()
    # injected_asgmt_file.unlink()


if __name__ == '__main__':
    """
    sys.argv[1]: assignment identifier as written in config.yml
    sys.argv[2]: path to the folder where assignments are saved (e.g. ~/Downloads)
    """
    asgmt_id = sys.argv[1]
    asgmt_folder = Path(sys.argv[2])
    try:
        # It expects only one .py file to be checked
        asgmt_file = next(asgmt_folder.glob('*.py'))
    except StopIteration:
        console.print(f'[dark_orange]No .py files found in {asgmt_folder}')
        sys.exit()

    handle_assignment(asgmt_id, asgmt_file)

import re
import subprocess
from pathlib import Path

import pyperclip
import services
import settings
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm

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
        exception_raised = True
    else:
        output = output.strip().split('\n')[-1]
        exception_raised = False
    code_works = output == desired_output
    return output, code_works, exception_raised


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


def handle_testbench_case(case: dict, injected_asgmt_file: Path):
    args = ' '.join(str(v) for v in case['input'])
    desired_output = ' '.join(str(v) for v in case['output'])
    output, code_works, exception_raised = run_test(
        injected_asgmt_file.name, args, desired_output
    )
    print('Desired output:', desired_output)
    color, symbol = settings.CORRECTION_DISPLAY[code_works][:2]
    console.print(f'[{color}]Program output: {output} {symbol}')
    return code_works, exception_raised


def contrib_feedback(asgmt_file: Path, feedback_cfg: dict):
    feedback_items = []
    code = asgmt_file.read_text()
    expected = feedback_cfg.get('expected', [])
    for item in expected:
        if not re.search(item['regex'], code):
            feedback_items.append(item)
    unexpected = feedback_cfg.get('unexpected', [])
    for item in unexpected:
        item['linenos'] = []
        for lineno, line in enumerate(code.split('\n')):
            if re.match(r'^\s*#.*', line):
                continue
            if re.search(item['regex'], line):
                item['linenos'].append(lineno + 1)
        if item['linenos']:
            feedback_items.append(item)
    return feedback_items


def handle_assignment(
    asgmt_file: Path,
    testbench: dict,
    global_feedback_cfg: dict = {},
    clean_files: bool = True,
):
    markdown = Markdown(f'# {asgmt_file.name}')
    console.print(markdown)

    securized_asgmt_file = create_securized_asgmt_file(asgmt_file)
    injected_asgmt_file = create_injected_asgmt_file(securized_asgmt_file, testbench)

    code_works, exception_raised = [], []
    for case in testbench['cases']:
        cw, er = handle_testbench_case(case, injected_asgmt_file)
        code_works.append(cw)
        exception_raised.append(er)

    services.show_testbench_results(code_works, settings.CORRECTION_DISPLAY)

    code_always_works = all(code_works)
    any_exception_raised = any(exception_raised)

    asgmt_feedback_cfg = testbench.get('feedback', {})
    feedback_cfg = services.merge_feedbacks_cfg(asgmt_feedback_cfg, global_feedback_cfg)

    if code_always_works and (user_feedback := contrib_feedback(asgmt_file, feedback_cfg)):
        pyperclip.copy(display_items := services.prepare_user_feedback(user_feedback))
        console.print(f'[orange_red1]Feedback:\n{display_items}')

    if Confirm.ask('Do you want to see the code?', default=True):
        file_to_show = injected_asgmt_file if any_exception_raised else asgmt_file
        services.show_code(file_to_show)

    if clean_files:
        console.print('[magenta]Cleaning temp files and assignment code...')
        services.clean_files(asgmt_file, securized_asgmt_file, injected_asgmt_file)

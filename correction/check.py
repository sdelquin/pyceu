import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

console = Console()

CORRECTION_DISPLAY = (
    ('red', '❌', 'NO APTO', '🙁'),
    ('green', '✅', 'APTO', '🥳'),
)


def parse_exception(exception_message):
    if m := re.search(r'\w+Error:.*', exception_message):
        return m.group()
    else:
        return 'Exception'


def run_test(filename, args, desired_output):
    command = f'python {filename} {args}'
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
    code = 'import sys\n\n' + code

    for i, var in enumerate(input_vars):
        if isinstance(var, dict):
            # typecast is set
            varname, cast = tuple(var.items())[0]
        else:
            varname, cast = var, 'str'
        code = re.sub(
            rf'{varname} *=.*', f'{varname} = {cast}(sys.argv[{i + 1}])', code, count=1
        )

    print_statements = []
    for varname in output_vars:
        print_statements.append(f"print(globals().get('{varname}', 'UNDEF'), end=' ')")
    print_statements = '\n'.join(print_statements)

    code = code + '\n' + print_statements + '\n'
    return code


def handle_assignment(asgmt_id, asgmt_filename):
    passed = []
    config = yaml.load(Path('config.yml').read_text(), Loader=yaml.FullLoader)[asgmt_id]
    asgmt_file = Path(asgmt_filename)
    asgmt_code = asgmt_file.read_text()
    injected_asgmt_code = inject_checking_code(
        asgmt_code, config['vars']['input'], config['vars']['output']
    )
    injected_asgmt_filename = asgmt_file.stem + '.injected' + asgmt_file.suffix
    injected_asgmt_file = Path(injected_asgmt_filename)
    injected_asgmt_file.write_text(injected_asgmt_code)
    for case in config['cases']:
        args = ' '.join(str(v) for v in case['input'])
        desired_output = ' '.join(str(v) for v in case['output'])
        output, code_works = run_test(injected_asgmt_filename, args, desired_output)
        print('Desired output:', desired_output)
        color, symbol = CORRECTION_DISPLAY[code_works][:2]
        console.print(f'[{color}]Program output: {output} {symbol}')
        passed.append(code_works)

    color, _, mark, symbol = CORRECTION_DISPLAY[all(passed)]
    print('-------------------------------------')
    console.print(f'[{color}]{mark} ({sum(passed)}/{len(passed)}) {symbol}')

    injected_asgmt_file.unlink()


def download_task(task_url):
    options = Options()
    options.headless = True

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', os.getcwd())
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
    profile.set_preference('pdfjs.disabled', True)

    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.get(task_url)

    element = driver.find_element_by_id('username')
    element.send_keys()  # GobCan CAS username
    element = driver.find_element_by_id('password')
    element.send_keys()  # GobCan CAS password
    element = driver.find_element_by_id('btn-login')
    element.click()

    os.rename('whatever.py', 'task.py')


if __name__ == '__main__':
    handle_assignment(sys.argv[1], sys.argv[2])

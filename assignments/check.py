import os
import re
import subprocess
import sys

from rich.console import Console
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from testingbench import get_bench

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


def run_test(task_filename, args):
    command = f'python {task_filename} {args}'
    console.print(f'[dark_goldenrod]INPUT: {command}')
    try:
        output = subprocess.check_output(
            command, encoding='utf-8', shell=True, stderr=subprocess.STDOUT
        )
    except Exception as err:
        output = parse_exception(err.output)
    else:
        output = output.strip().split('\n')[-1]
    return output


def handle_task(task_id, task_filename):
    os.environ['CHECK'] = '1'
    passed = []
    for args, desired_output in get_bench(task_id):
        args = ' '.join(args)
        desired_output = ' '.join(desired_output)
        output = run_test(task_filename, args)
        print('Desired output:', desired_output)
        is_right_task = output == desired_output
        color, symbol = CORRECTION_DISPLAY[is_right_task][:2]
        passed.append(is_right_task)
        console.print(f'[{color}]Program output: {output} {symbol}')

    color, _, mark, symbol = CORRECTION_DISPLAY[all(passed)]
    print('-------------------------------------')
    console.print(f'[{color}]{mark} ({sum(passed)}/{len(passed)}) {symbol}')


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
    handle_task(sys.argv[1], sys.argv[2])

import re
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import pyperclip
import services
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm

CORRECTION_DISPLAY = (
    ('red', '❌', 'NO APTO', '🙁'),
    ('green', '✅', 'APTO', '🥳'),
)


class AsgmtError(Exception):
    pass


class Marker:
    def __init__(self, asgmt_file: Path, config_file: Path):
        self.asgmt_file = asgmt_file
        self.config_file = config_file

        self.asgmt_code = self.asgmt_file.read_text()
        self.config = yaml.load(self.config_file.read_text(), Loader=yaml.FullLoader)

        if not (asgmt_id := services.get_asgmt_id(self.asgmt_code)):
            raise AsgmtError('Assignment id was not found on input file')
        if asgmt_id not in self.config['testbench']:
            raise AsgmtError(f'Assignment id "{asgmt_id}" is not valid')
        self.testbench_cfg = self.config['testbench'][asgmt_id]
        self.feedback_cfg = self.testbench_cfg.get('feedback', {})
        self.global_cfg = self.config.get('global', {})
        self.global_feedback_cfg = self.global_cfg.get('feedback', {})

        self.console = Console()

        self.injected_asgmt_file = self.create_injected_asgmt_file()

    def run_test(self, args: str, desired_output: list[str]):
        command = f'python "{self.injected_asgmt_file}" {args}'
        self.console.print(f'[bold cyan]$ {command}')
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

    def create_injected_asgmt_file(self):
        self.console.print('[magenta]Injecting testing code...')
        securized_code = services.securize_code(self.asgmt_code)
        injected_asgmt_code = services.inject_checking_code(
            securized_code,
            self.testbench_cfg['vars']['input'],
            self.testbench_cfg['vars']['output'],
        )
        injected_asgmt_file = Path(NamedTemporaryFile().name)
        injected_asgmt_file.write_text(injected_asgmt_code)
        return injected_asgmt_file

    def handle_testbench_case(self, testcase: dict):
        args = ' '.join(f'"{str(v)}"' for v in testcase['input'])
        desired_output = ' '.join(str(v) for v in testcase['output'])
        output, code_works, exception_raised = self.run_test(args, desired_output)
        print('Desired output:', desired_output)
        color, symbol = CORRECTION_DISPLAY[code_works][:2]
        self.console.print(f'[{color}]Program output: {output} {symbol}')
        return code_works, exception_raised

    def get_runtime_feedback(self):
        self.console.print('[magenta]Getting runtime feedback...')
        feedback_items = []
        expected = self.feedback_cfg.get('expected', [])
        for item in expected:
            if not re.search(item['regex'], self.asgmt_code):
                feedback_items.append(item)
        unexpected = self.feedback_cfg.get('unexpected', [])
        for line in self.asgmt_code.split('\n'):
            if re.match(r'^\s*#.*', line):
                continue
            for item in unexpected:
                if re.search(item['regex'], line):
                    feedback_items.append(item)
        return feedback_items

    def get_style_feedback(self):
        self.console.print('[magenta]Getting style feedback...')
        command = f'flake8 "{self.asgmt_file}"'
        return subprocess.run(
            command,
            capture_output=True,
            encoding='utf-8',
            shell=True,
            check=False,
        ).stdout

    def manage_feedback(self):
        buffer = []
        runtime_feedback = self.get_runtime_feedback()
        style_feedback = self.get_style_feedback()
        feedbacks_items = services.prepare_runtime_feedback(runtime_feedback)
        style_items = services.prepare_style_feedback(style_feedback)

        if feedbacks_items:
            buffer.append(feedbacks_items)
        if style_items:
            buffer.append(style_items)

        if feedbacks_items or style_items:
            if Confirm.ask('Do you want to see the feedback?', default=True):
                if feedbacks_items:
                    self.console.print(f'[orange_red1]{feedbacks_items}')
                if style_items:
                    self.console.print(f'[orange_red1]{style_items}')

        return '\n\n'.join(buffer)

    def manage_code(self, code_always_works, any_exception_raised):
        file_to_show = self.injected_asgmt_file if any_exception_raised else self.asgmt_file
        services.show_code(file_to_show)
        if code_always_works and Confirm.ask(
            'Do you want to add language feedback?', default=False
        ):
            self.console.print('[magenta]Getting language feedback...')
            lang_feedback = services.prepare_lang_feedback(
                self.global_feedback_cfg.get('lang-message')
            )
            self.console.print(f'[orange_red1]{lang_feedback}')
            return lang_feedback
        return ''

    def handle_assignment(self):
        self.console.print(Markdown(f'# {self.asgmt_file}'))

        code_works, exception_raised = [], []
        for testcase in self.testbench_cfg['cases']:
            cw, er = self.handle_testbench_case(testcase)
            code_works.append(cw)
            exception_raised.append(er)

        services.show_testbench_results(code_works, CORRECTION_DISPLAY)

        code_always_works, any_exception_raised = all(code_works), any(exception_raised)
        clipboard = []

        if code_always_works:
            clipboard.append(self.manage_feedback())

        if Confirm.ask('Do you want to see the code?', default=True):
            clipboard.append(self.manage_code(code_always_works, any_exception_raised))

        self.console.print('[magenta]Copying feedback to clipboard...')
        pyperclip.copy('\n\n'.join(clipboard).strip())

        self.injected_asgmt_file.unlink()

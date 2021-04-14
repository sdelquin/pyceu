import re
import subprocess
from pathlib import Path

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


class Marker:
    def __init__(self, asgmt_file: Path, config_file: Path, asgmt_id: str):
        self.asgmt_file = asgmt_file
        self.config_file = config_file

        self.asgmt_code = self.asgmt_file.read_text()
        self.config = yaml.load(self.config_file.read_text(), Loader=yaml.FullLoader)

        self.testbench_cfg = self.config['testbench'][asgmt_id]
        self.feedback_cfg = self.testbench_cfg.get('feedback', {})
        self.global_cfg = self.config.get('global', {})
        self.global_feedback_cfg = self.global_cfg.get('feedback', {})

        self.console = Console()

        self.securized_asgmt_file = self.create_securized_asgmt_file()
        self.injected_asgmt_file = self.create_injected_asgmt_file()

    def run_test(self, args: list[str], desired_output: list[str]):
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

    @staticmethod
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

    def create_injected_asgmt_file(self):
        self.console.print('[magenta]Injecting testing code...')
        injected_asgmt_code = Marker.inject_checking_code(
            self.asgmt_code,
            self.testbench_cfg['vars']['input'],
            self.testbench_cfg['vars']['output'],
        )
        injected_asgmt_filename = (
            self.asgmt_file.stem + '.injected' + self.asgmt_file.suffix
        )
        injected_asgmt_file = Path(injected_asgmt_filename)
        injected_asgmt_file.write_text(injected_asgmt_code)
        return injected_asgmt_file

    @staticmethod
    def securize_code(code: str):
        securized_code = []
        for line in code.split('\n'):
            if re.search(r'\bimport\b', line):
                securized_line = '# ' + line
            else:
                securized_line = line
            securized_code.append(securized_line)
        return '\n'.join(securized_code)

    def create_securized_asgmt_file(self):
        self.console.print('[magenta]Securizing input code...')
        securized_asgmt_code = Marker.securize_code(self.asgmt_code)
        securized_asgmt_filename = (
            self.asgmt_file.stem + '.securized' + self.asgmt_file.suffix
        )
        securized_asgmt_file = Path(securized_asgmt_filename)
        securized_asgmt_file.write_text(securized_asgmt_code)
        return securized_asgmt_file

    def handle_testbench_case(self, testcase: dict):
        args = ' '.join(str(v) for v in testcase['input'])
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

    def handle_assignment(self, clean_files: bool = True):
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
            runtime_feedback = self.get_runtime_feedback()
            style_feedback = self.get_style_feedback()
            feedbacks_items = services.prepare_runtime_feedback(runtime_feedback)
            style_items = services.prepare_style_feedback(style_feedback)
            if feedbacks_items:
                self.console.print(f'[orange_red1]{feedbacks_items}')
                clipboard.append(feedbacks_items)
            if style_items:
                self.console.print(f'[orange_red1]{style_items}')
                clipboard.append(style_items)

        if Confirm.ask('Do you want to see the code?', default=True):
            file_to_show = (
                self.injected_asgmt_file if any_exception_raised else self.asgmt_file
            )
            services.show_code(file_to_show)
            if code_always_works and Confirm.ask(
                'Do you want to add language feedback?', default=True
            ):
                lang_feedback = services.prepare_lang_feedback(
                    self.global_feedback_cfg.get('lang-message')
                )
                self.console.print(f'[orange_red1]{lang_feedback}')
                clipboard.append(lang_feedback)

        if clean_files:
            self.console.print('[magenta]Cleaning temp files and assignment code...')
            services.clean_files(
                self.asgmt_file, self.securized_asgmt_file, self.injected_asgmt_file
            )

        self.console.print('[magenta]Copying feedback to clipboard...')
        pyperclip.copy('\n\n'.join(clipboard))

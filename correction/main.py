#!/usr/bin/env python
from pathlib import Path

import services
import settings
import typer
from check import handle_assignment
from rich.console import Console

console = Console()
app = typer.Typer(add_completion=False)


@app.command()
def check(
    asgmt_id: str = typer.Argument(
        ..., help='Assignment identifier as written in testbench (e.g. dicts)'
    ),
    asgmt_folder_path: str = typer.Argument(
        ..., help='Path to the folder where assignments are saved (e.g. ~/Downloads)'
    ),
    keep_files: bool = typer.Option(
        False, '-k', help='Do not remove input file (and injected code) after execution'
    ),
):
    '''Check assignments'''
    try:
        testbench = services.read_testbench(settings.TESTBENCH, asgmt_id)
    except FileNotFoundError:
        services.show_error(f'Testbench file "{settings.TESTBENCH}" not found!')
    except KeyError:
        services.show_error(f'Assignment id "{asgmt_id}" not found!')
    else:
        asgmt_folder = Path(asgmt_folder_path)
        try:
            # It expects only one .py file to be checked
            asgmt_file = next(asgmt_folder.glob('*.py'))
        except StopIteration:
            services.show_error(f'No .py files found in {asgmt_folder}')
        else:
            handle_assignment(asgmt_file, testbench, clean_files=not keep_files)


@app.command()
def list_asgmts():
    '''List available assignments identifiers on testbench'''
    testbench = services.read_testbench(settings.TESTBENCH)
    services.show_testbench(testbench)


if __name__ == '__main__':
    app()

#!/usr/bin/env python
from pathlib import Path

import services
import typer
from check import handle_assignment
from rich.console import Console
from rich.table import Table

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
    asgmt_folder = Path(asgmt_folder_path)
    try:
        # It expects only one .py file to be checked
        asgmt_file = next(asgmt_folder.glob('*.py'))
    except StopIteration:
        services.show_error(f'No .py files found in {asgmt_folder}')
    else:
        handle_assignment(asgmt_id, asgmt_file, not keep_files)


@app.command()
def list_asgmts():
    '''List available assignments identifiers on testbench'''
    testbench = services.read_testbench()

    table = Table(title='Available assignments')
    table.add_column("id", justify="right", style="cyan", no_wrap=True)
    table.add_column("title", justify="left", style="magenta", no_wrap=True)
    for asgmt_id, data in testbench.items():
        table.add_row(asgmt_id, data['title'])
    console.print(table)


if __name__ == '__main__':
    app()

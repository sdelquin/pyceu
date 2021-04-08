#!/usr/bin/env python
from pathlib import Path

import typer
from rich.console import Console

import asgmt

console = Console()


def main(
    asgmt_id: str = typer.Argument(
        ..., help='Assignment identifier as written in config.yml'
    ),
    asgmt_folder_path: str = typer.Argument(
        ..., help='Path to the folder where assignments are saved (e.g. ~/Downloads)'
    ),
    keep_files: bool = typer.Option(
        False, '-k', help='Do not remove input file (and injected code) after execution'
    ),
):
    asgmt_folder = Path(asgmt_folder_path)
    try:
        # It expects only one .py file to be checked
        asgmt_file = next(asgmt_folder.glob('*.py'))
    except StopIteration:
        console.print(f'[orange_red1]⚠️  No .py files found in {asgmt_folder}')
    else:
        asgmt.handle_assignment(asgmt_id, asgmt_file, not keep_files)


if __name__ == '__main__':
    # https://bit.ly/3t2hLRx
    app = typer.Typer(add_completion=False)
    app.command()(main)
    app()

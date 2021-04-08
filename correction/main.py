#!/usr/bin/env python
from pathlib import Path

import typer
import yaml
from check import handle_assignment
from rich.console import Console

console = Console()
app = typer.Typer(add_completion=False)


@app.command()
def check(
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
    '''Check assignments'''
    asgmt_folder = Path(asgmt_folder_path)
    try:
        # It expects only one .py file to be checked
        asgmt_file = next(asgmt_folder.glob('*.py'))
    except StopIteration:
        console.print(f'[orange_red1]⚠️  No .py files found in {asgmt_folder}')
    else:
        handle_assignment(asgmt_id, asgmt_file, not keep_files)


@app.command()
def list_asgmts():
    '''List available assignments identifiers'''
    config = yaml.load(Path('config.yml').read_text(), Loader=yaml.FullLoader)
    asgmts_ids = '\n'.join(config.keys())
    print(asgmts_ids)


if __name__ == '__main__':
    app()

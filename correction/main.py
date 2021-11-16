#!/usr/bin/env python
from pathlib import Path

import services
import settings
import typer
from rich.console import Console

from correction import Marker

console = Console()
app = typer.Typer(add_completion=False)


@app.command()
def check(
    asgmt_target_path: str = typer.Option(
        settings.ASGMT_FOLDER_PATH,
        '--target',
        '-t',
        help='Target to file or folder where the assignments are taken from. '
        'In case of a folder, only the newest .py file is taken',
    ),
):
    '''Check assignments'''
    if asgmt_file := services.get_asgmt_file(Path(asgmt_target_path)):
        try:
            marker = Marker(asgmt_file, Path(settings.CONFIG_FILE))
        except AttributeError as err:
            services.show_error(err)
        else:
            marker.handle_assignment()
    else:
        services.show_error(f'No .py files found in {asgmt_target_path}')


@app.command()
def list_asgmts():
    '''List available assignments identifiers on testbench'''
    services.list_asgmts(settings.CONFIG_FILE)


if __name__ == '__main__':
    app()

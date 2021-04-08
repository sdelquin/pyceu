from pathlib import Path

import settings
import yaml


def read_testbench(filepath: str = settings.TESTBENCH):
    return yaml.load(Path(filepath).read_text(), Loader=yaml.FullLoader)

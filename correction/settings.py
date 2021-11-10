from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_FILE = config('CONFIG_FILE', default='config.yml')
ASGMT_FOLDER_PATH = config('ASGMT_FOLDER_PATH', default=PROJECT_DIR / 'tmp', cast=Path)

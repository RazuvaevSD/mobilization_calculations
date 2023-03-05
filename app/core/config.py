import os
from enum import Enum

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_URI = os.getenv('DB_URI', 'sqlite:///story.db')


class WindowConf(str, Enum):
    SIZE = '1000x800'
    TITLE = 'Мобилизационные расчеты'

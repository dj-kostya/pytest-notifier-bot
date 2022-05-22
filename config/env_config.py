import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TO_JSON_REPORT = os.path.join(Path(__file__).parent.parent, '.report.json')

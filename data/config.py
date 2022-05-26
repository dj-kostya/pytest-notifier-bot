import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDB = os.getenv('PGDB')

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
TESTS_PATH = os.getenv("TESTS_PATH")
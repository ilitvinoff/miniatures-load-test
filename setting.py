import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BASE_URL = os.getenv("BASE_URL", None)
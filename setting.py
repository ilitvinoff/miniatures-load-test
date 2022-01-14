import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BASE_URL = os.getenv("BASE_URL", None)
NUM_USERS = int(os.getenv("NUM_USERS", None))
SPAWN_RATE = int(os.getenv("SPAWN_RATE", None))
RUN_TIME = os.getenv("RUN_TIME", None)
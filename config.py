import os

from dotenv import load_dotenv

load_dotenv()


DATA_DIR_PATH = r"D:\ildar\python-training\data"

# BOT
TOKEN = os.getenv("TOKEN")

# DB
DB_URL = os.getenv("DATABASE_URL")

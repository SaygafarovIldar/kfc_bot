import os

from dotenv import load_dotenv

load_dotenv()


DATA_DIR_PATH = r"D:\ildar\python-training\data"

# BOT
TOKEN = os.getenv("TOKEN")

# DB
IP = os.getenv("IP")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{IP}/{DB_NAME}"

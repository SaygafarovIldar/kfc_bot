import json
import os

from aiogram import Dispatcher

from bot.loader import db
from config import DB_URL
from utils.db_api.main import Product


def data_from_file(dir_path: str):
    """Получаем данные из json файлов."""
    res = []
    for file_name in os.listdir(dir_path):
        if file_name != "location":
            with open(f"{dir_path}/{file_name}", "r", encoding="utf-8") as file:
                res.append(json.load(file))
    return res


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(DB_URL)
    await db.gino.create_all()


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )

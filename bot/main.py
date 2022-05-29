from aiogram import Dispatcher

from bot.loader import db
from config import DB_URL


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(DB_URL)


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )

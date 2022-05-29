from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.fsm.menu import OrderState
from bot.keyboards import main_menu_keyboard, categories_keyboard, meals_keyboard
from loader import dp, bot
from utils.db_api.main import Category, Product


@dp.message_handler(commands='start')
async def start_handler(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Добро пожаловать в бота КФС, выбери действие ниже ⬇",
                           reply_markup=main_menu_keyboard())


@dp.message_handler(text=["Меню"])
async def process_categories(message: types.Message) -> None:
    await OrderState.category.set()
    categories = await Category.get_categories()
    await bot.send_message(message.chat.id, "Выберите категорию", reply_markup=categories_keyboard(categories))


@dp.message_handler(state=OrderState.category)
async def process_meal(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["category"] = message.text

    meals = await Product.get_products(data["category"])
    cat_id = await Category.get_category_id(data["category"])
    await OrderState.next()
    await bot.send_message(message.chat.id, "Выберите блюдо", reply_markup=meals_keyboard(meals, cat_id))


@dp.message_handler(state=OrderState.meal)
async def show_meal(message: types.Message, state: FSMContext) -> None:
    """Показываем пользователю то блюдо, которое он выбрал."""
    await OrderState.next()
    product_info = await Product.get_product(message.text)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=product_info.get("image_url"),
        caption=f"""
Название: {product_info.get("name")}
Описание: {product_info.get("description")}
Цена: {product_info.get("price")}
"""
    )
    # await state.update_data(meal=)

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from bot import keyboards
from bot.fsm.menu import OrderState
from loader import dp, bot
from utils.db_api.main import Category, Product


@dp.message_handler(commands='start')
async def start_handler(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Добро пожаловать в бота КФС, выбери действие ниже ⬇",
                           reply_markup=keyboards.main_menu_keyboard())


@dp.message_handler(text=["Меню"])
async def process_categories(message: types.Message) -> None:
    await OrderState.category.set()
    categories = await Category.get_categories()
    await bot.send_message(message.chat.id, "Выберите категорию",
                           reply_markup=keyboards.categories_keyboard(categories))


@dp.message_handler(state=OrderState.category)
async def process_meal(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["category"] = message.text
    meals = await Product.get_products(data["category"])
    cat_id = await Category.get_category_id(data["category"])
    await OrderState.next()
    await bot.send_message(message.chat.id, "Выберите блюдо", reply_markup=keyboards.meals_keyboard(meals, cat_id))


@dp.message_handler(state=OrderState.meal)
async def show_meal(message: types.Message, state: FSMContext) -> None:
    """Показываем пользователю то блюдо, которое он выбрал."""
    await OrderState.next()
    if message.text != "Назад⬅":
        product_info = await Product.get_product(message.text)
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=product_info.get("image_url"),
            caption=f"""
<b>Название</b>: <i>{product_info.get("name")}</i>
<b>Описание</b>: <i>{product_info.get("description")}</i>
<b>Цена</b>: <i>{product_info.get("price")}</i>
""",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.to_cart_keyboard()
        )
        await state.set_state(OrderState.meal)
    else:
        await state.set_state(OrderState.category)
        categories = await Category.get_categories()
        await bot.send_message(message.from_user.id, "Выберите категорию",
                               reply_markup=keyboards.categories_keyboard(categories))

# @dp.callback_query_handler(lambda call: call.data == "to_cart", state=MakingOrderState.confirmation)
# async def make_order(query: types.CallbackQuery, state: FSMContext):
#     """Создание заказа."""
#     await MakingOrderState.next()
#     await query.message.answer(text="Ваш заказ", reply_markup=keyboards.making_order_keyboard())
#
#
# @dp.message_handler(state=MakingOrderState.confirm)
# async def confirm(message: types.Message, state: FSMContext):
#     if message.text == "Назад⬅":
#         await state.set_state(OrderState.meal)
#         categories = await Category.get_categories()
#         await bot.send_message(message.chat.id, "Выберите блюдо",
#                                reply_markup=keyboards.categories_keyboard(categories))

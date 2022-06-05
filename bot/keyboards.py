from aiogram import types


def main_menu_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Меню"))
    return keyboard


def categories_keyboard(categories_data: list[str]) -> types.ReplyKeyboardMarkup:
    """Меню с кнопками категорий."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text=category) for category in categories_data]
    keyboard.add(*buttons)
    buttons.append(types.KeyboardButton(text="Назад ⬅"))
    return keyboard


def meals_keyboard(products_data, category_id=None):
    """Меню с кнопками всех блюд."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(text=item.get("name")) for item in products_data
               if item.get("category") == category_id]
    buttons.append(types.KeyboardButton(text="Назад ⬅"))
    keyboard.add(*buttons)
    return keyboard


def to_cart_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Добавить в корзину", callback_data="to_cart")
    keyboard.add(button)
    return keyboard


def making_order_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton(text="Да ✅"),
        types.KeyboardButton(text="Нет ❌"),
        types.KeyboardButton(text="Назад ⬅")
    ]
    keyboard.add(*buttons)
    return keyboard

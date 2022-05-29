from aiogram import types


def main_menu_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    content = ["Меню", "История заказов"]
    buttons = [types.KeyboardButton(text=item) for item in content]
    keyboard.add(*buttons)
    return keyboard


def categories_keyboard(categories_data: list[str]) -> types.ReplyKeyboardMarkup:
    """Меню с кнопками категорий."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = [types.KeyboardButton(text=category) for category in categories_data]
    keyboard.add(*categories)
    return keyboard


def meals_keyboard(products_data, category_id=None):
    """Меню с кнопками всех блюд."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(text=item.get("name")) for item in products_data
               if item.get("category") == category_id]
    keyboard.add(*buttons)
    return keyboard

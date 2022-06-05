from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    """OrderState."""
    menu = State()
    category = State()
    meal = State()
    wait = State()
    add_to_cart = State()


# class MakingOrderState(StatesGroup):
#     """MakingOrderState."""
#     confirmation = State()
#     confirm = State()

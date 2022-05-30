from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    """OrderState."""
    category = State()
    meal = State()


class MakingOrderState(StatesGroup):
    """MakingOrderState."""
    confirmation = State()
    confirm = State()

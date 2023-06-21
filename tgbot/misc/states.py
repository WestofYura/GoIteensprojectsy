from aiogram.dispatcher.filters.state import StatesGroup, State


class ConvertCurrencyStates(StatesGroup):
    waiting_for_source_currency = State()
    waiting_for_target_currency = State()
    waiting_for_amount = State()

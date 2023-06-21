import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot.keyboards.reply import keyboard
from tgbot.misc.states import ConvertCurrencyStates


async def cmd_start(message: types.Message):

    await message.answer("Привіт👋🏻! Я бот для конвертації валют.\n/convert: почати ковертувати\nСписок валют:\nUSD$ - долари\nUAH₴ -- гривні\nEUR€ -- Євро\nPLN -- грош(польща)\nRUB -- рублі\nGBP -- пенні(Велика Британія)\nBYN -- копійка(білорусь)\nKGS -- киргизький сом\nCNY -- китайський юань", reply_markup=keyboard)



async def cmd_help(message: types.Message):
    await message.answer("За допомогою до адміна: @qwerix_fort")





async def cmd_convert(message: types.Message):
    await message.answer("Введіть вихідну валюту (наприклад, USD):")
    await ConvertCurrencyStates.waiting_for_source_currency.set()




async def process_source_currency(message: types.Message, state: FSMContext):
    source_currency = message.text.upper()

    await state.update_data(source_currency=source_currency)

    await message.answer("Введіть цільову валюту (наприклад, EUR):")
    await ConvertCurrencyStates.waiting_for_target_currency.set()




async def process_target_currency(message: types.Message, state: FSMContext):
    target_currency = message.text.upper()

    await state.update_data(target_currency=target_currency)

    await message.answer("Введіть сумму конвертації:")
    await ConvertCurrencyStates.waiting_for_amount.set()




async def process_amount(message: types.Message, state: FSMContext):
    amount = message.text

    data = await state.get_data()
    source_currency = data['source_currency']
    target_currency = data['target_currency']

    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{source_currency}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        conversion_rate = data['rates'][target_currency]
        converted_amount = float(amount) * conversion_rate

        await message.answer(f"✅Виконано✅:\n{amount} {source_currency} = {converted_amount} {target_currency}")
    except (Exception,KeyError):
        await message.answer("Виникла помилка при конвертації валют")

    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(cmd_start,Command("start"))
    dp.register_message_handler(cmd_help,Command("help"))
    dp.register_message_handler(cmd_convert,Command("convert"))
    dp.register_message_handler(process_source_currency,state=ConvertCurrencyStates.waiting_for_source_currency)
    dp.register_message_handler(process_target_currency,state=ConvertCurrencyStates.waiting_for_target_currency)
    dp.register_message_handler(process_amount,state=ConvertCurrencyStates.waiting_for_amount)


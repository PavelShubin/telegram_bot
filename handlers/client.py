from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Вс-чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')

# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message : types.Message):
    pass

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
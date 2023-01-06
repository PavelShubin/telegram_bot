from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot

ID = 1012783008

class FSMAdmin(StatesGroup):
    moderator = State()
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands=['moderator'])
async def make_changes_command(message : types.Message):
    global ID
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Что тебе нужно?')
        await FSMAdmin.moderator.set()
        await message.delete()

# Начало диалога
# @dp.message_handler(commands='Загрузить', state=FSMAdmin.moderator)
async def cm_start(message : types.Message, state):
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')

# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Теперь введи название')

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание')

# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь укажи цену')

# Ловим последний ответ и используем полученный данные
# @dp.message_handler(FSMAdmin.price)
async def load_price(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()

# @dp.message_handler(state="*", commands=['Отмена'])
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await FSMAdmin.moderator.set()
    await message.reply('ОК')

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=FSMAdmin.moderator)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

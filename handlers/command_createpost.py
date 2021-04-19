from aiogram import types
from misc import dp, bot
from .another_sqlit import check_channels
from .generate_post import get_post

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

@dp.callback_query_handler(text_startswith='apps_chanals', state='*')
async def appchanels1(call: types.callback_query,state: FSMContext):
    data = await state.get_data()
    message = data['message']
    m2 = data['m2']

    channel = call.data[12:]
    await bot.delete_message(chat_id=m2.chat.id, message_id=m2.message_id)
    await get_post(channel, message, state=state)

@dp.message_handler(commands="post")
async def add_channel(message: types.message,state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    bat1 = types.InlineKeyboardButton(text='Отправить', callback_data="send_post")
    markup.add(bat1)
    a = check_channels(message.chat.id) # Получение списка каналов, где человек является админом
    massiv_channel = [] # Список каналов, где человек админ

    await state.update_data(message=message)# Добавление message для веше хендлера

    for i in a:
        if i[0] != None and i[0]!= 0:
            massiv_channel.append(i[0])

    if len(massiv_channel) == 0:
        await bot.send_message(chat_id=message.chat.id,text="Сначала добавь свой канал с помощью команды:\n"
                                                            "/addchannel")

    if len(massiv_channel) == 1 :
        await get_post(massiv_channel[0],message,state= state)

    if len(massiv_channel) >= 2 :
        markup = types.InlineKeyboardMarkup()
        for i in range(len(massiv_channel)):
            bat = types.InlineKeyboardButton(text=f'{massiv_channel[i]}', callback_data= f'apps_chanals{massiv_channel[i]}')
            markup.add(bat)
        m2 = await bot.send_message(chat_id=message.chat.id, text='Выберите канал для создания поста:',reply_markup=markup)
        await state.update_data(m2=m2)  # Удаление смс






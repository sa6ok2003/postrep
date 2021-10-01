from aiogram import types
from misc import dp, bot
import sqlite3

import asyncio

from aiogram.dispatcher import FSMContext
from .sqlit import red_goodchannel,info_members,reg_one_channel,info_channel,del_one_channel
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 941730379 #Джейсон
ADMIN_ID_4 = 678623761 # Бекир


ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3,ADMIN_ID_4]

class reg1(StatesGroup):
    name1 = State()
    fname1 = State()



@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        red_goodchannel(1)

        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='Добавить канал', callback_data='new_channel')
        bat_c = types.InlineKeyboardButton(text='Удалить канал', callback_data='delite_channel')
        bat_d = types.InlineKeyboardButton(text='Список каналов', callback_data='list_channel')
        bat_e = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        markup.add(bat_a)
        markup.add(bat_b,bat_c)
        markup.add(bat_d)
        markup.add(bat_e)

        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = info_members() # Вызов функции из файла sqlit
        await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')

@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        a = open('server.db','rb')
        await bot.send_document(chat_id=call.message.chat.id, document=a)




############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                     '@name_channel')
        await reg1.name1.set()


@dp.message_handler(state=reg1.name1, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        check_dog = message.text[:1]
        if check_dog != '@':
            await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
        else:
            reg_one_channel(message.text)
            await bot.send_message(message.chat.id, 'Регистрация успешна')
            await state.finish()


@dp.callback_query_handler(text='list_channel')
async def check(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        mes= ''
        a = info_channel()
        for i in range(len(a)):
            mes+= '@'+ str(a[i][0])+ '\n'

        await bot.send_message(call.message.chat.id,text=mes)


@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    if call.message.chat.id in ADMIN_ID:
        await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                     '@name_channel')
        await reg1.fname1.set()


@dp.message_handler(state=reg1.fname1, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    if message.chat.id in ADMIN_ID:
        check_dog = message.text[:1]
        if check_dog != '@':
            await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
        else:
            await state.finish()
            del_one_channel(message.text)
            await bot.send_message(message.chat.id, 'Удаление завершено')
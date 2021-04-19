from aiogram import types
from misc import dp, bot
from aiogram.dispatcher import FSMContext
import sqlite3
from aiogram.dispatcher.filters.state import State, StatesGroup

@dp.callback_query_handler(text_startswith='123')  # Нажал кнопку Начать смотреть
async def start_watch(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text='Я работаю')


@dp.callback_query_handler(text_startswith='tap_dable', state='*')
async def tap_bat_dable(call: types.callback_query,state: FSMContext):
    try:
        db = sqlite3.connect('server.db')
        sql = db.cursor()

        id_mes = call.message.message_id
        id_chat = call.message.chat.id

        # Обработка параметров
        text = (call.data[10:])
        arr = text.split('+')


        text_not_sub = ((sql.execute(f"SELECT text_bad FROM user_bat WHERE id_messad = {id_mes} and id_channel = {id_chat}")).fetchone())[0]
        text_sub = ((sql.execute(f"SELECT text_ok FROM user_bat WHERE id_messad = {id_mes} and id_channel = {id_chat}")).fetchone())[0]


        if call.message.sender_chat == None: #Человек нажал на кнопку в боте
            await bot.answer_callback_query(callback_query_id=call.id, text='Кнопка станет активной после того как ты опубликуешь пост в свой канал', show_alert=True)
        else:
            proverka = (await bot.get_chat_member(chat_id=id_chat, user_id=call.from_user.id)).status
            if proverka == 'left':# Отправка уведомления для левый чуваков
                await bot.answer_callback_query(callback_query_id=call.id,text=text_not_sub,show_alert=True)

            else:# Человек подписан на канал
                await bot.answer_callback_query(callback_query_id=call.id, text=text_sub, show_alert=True)

    except: await bot.answer_callback_query(callback_query_id=call.id, text='Кнопка станет активной после того как ты опубликуешь пост в свой канал', show_alert=True)

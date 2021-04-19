from aiogram import types
from misc import dp, bot

@dp.callback_query_handler(text_startswith='xxxxx')  # Нажал кнопку Начать смотреть
async def start_watch(call: types.callback_query):
    await bot.send_message(call.message.chat.id, text='Я работаю')

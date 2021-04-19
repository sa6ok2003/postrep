from aiogram import types
from misc import dp, bot
import asyncio

from .sqlit import update_user,proverka

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class reg(StatesGroup):
    name = State()
    fname = State()


@dp.callback_query_handler(text ='solve_set', state='*')
async def solveset(call: types.callback_query, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(commands="addchannel")
async def add_channel(message: types.message, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    opmena = types.InlineKeyboardButton(text='Отмена регистрации',callback_data='solve_set')
    markup.add(opmena)
    m1 =await bot.send_message(chat_id=message.chat.id, text= "Добавь меня Админом в свой канал, а затем перешли мне любое сообщение из своего канала!",reply_markup=markup)
    await state.update_data(m1=m1)
    await reg.name.set()



@dp.message_handler(state=reg.name, content_types=['text','photo','video','voice'])
async def name_channel(message: types.Message, state: FSMContext):
    user_name = message.forward_from_chat.username
    proverka(user_name)

    data = await state.get_data()
    m1 = data['m1']

    if message.text == '0':
        await state.finish()
        mes = await bot.send_message(message.chat.id, text= 'Отменено')
        await asyncio.sleep(10)
        await bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=m1.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


    else:
        user_name = message.forward_from_chat.username
        if user_name != None:
            try :
                user_name = message.forward_from_chat.username
                if proverka(user_name) == 1:
                    id_channel = (message.forward_from_chat.id)  # Запись id канала пользователя
                    a = await bot.get_chat_administrators(id_channel)
                    massiv_admin = []  # Содает массив админов в канале пользователя
                    for i in a:
                        if i.status == "administrator" or i.status == 'creator':
                            massiv_admin.append(i.user.id)

                    if message.chat.id in massiv_admin:
                        update_user(message.chat.id,id_channel,user_name)
                        await bot.send_message(chat_id=message.chat.id, text= f"Канал добавлен, теперь ты можешь начать создание поста: /post") # Регистрация в БД
                        await state.finish()
                        await bot.delete_message(chat_id=message.chat.id, message_id=m1.message_id)
                        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

                    else:
                        await bot.send_message(chat_id=message.chat.id, text= "Сначала добавьте меня в свой канал и назначь администратором!\n\n"
                                                            "После этого снова отправь мне любое сообщение из твоего канала\n"
                                                            "Для отмены - напиши 0")
                else:
                    await bot.send_message(chat_id=message.chat.id,text='Это приватный бот, доступ к нему платный.\n\n'
                                                                        'Подробности : @sanyar_boy',parse_mode='html')
                    await state.finish()

            except:
                await bot.send_message(message.chat.id, "Сначала добавьте меня в свой канал и назначь администратором!\n\n"
                                                        "После этого снова отправь мне любое сообщение из твоего канала\n"
                                                        "Для отмены - напиши 0")
        else:
            await bot.send_message(message.chat.id,
                                   "Проверь что твой канал публичный!!\n"
                                   "После этого снова отправь мне любое сообщение из твоего канала\n\n"
                                   "Для отмены - напиши 0")


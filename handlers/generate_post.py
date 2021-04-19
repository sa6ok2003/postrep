from aiogram import types
from misc import dp, bot
from .another_sqlit import return_chatid_channel
from .option_button import optioon_but, optioon_duble_button

import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .text_mes import text_but, text_but2,text_but3

import asyncio


class gener_post(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()
    step4 = State()
    step5 = State()
    gener_text = State()
    add_media = State()
    add_button = State()


markup = types.InlineKeyboardMarkup()
bat1 = types.InlineKeyboardButton(text='Опубликовать', callback_data="send_post")
bat2 = types.InlineKeyboardButton(text='Начать сначала', callback_data="start_new")
markup.add(bat1)
markup.add(bat2)

markup2 = types.InlineKeyboardMarkup()
bat1 = types.InlineKeyboardButton(text='Опубликовать', callback_data="send_post")
bat2 = types.InlineKeyboardButton(text='Начать сначала', callback_data="start_new")
bat3 = types.InlineKeyboardButton(text='Далее', callback_data="create_dable")
markup2.add(bat1)
markup2.add(bat2)
markup2.add(bat3)


markup3 = types.InlineKeyboardMarkup()
bat1 = types.InlineKeyboardButton(text='Опубликовать', callback_data="send_post")
bat2 = types.InlineKeyboardButton(text='Начать сначала', callback_data="start_new")
bat3 = types.InlineKeyboardButton(text='Далее', callback_data="create_reak")
markup3.add(bat1)
markup3.add(bat2)
markup3.add(bat3)


@dp.callback_query_handler(text='cansel', state=gener_post.step1)
async def otmena_vsego(call: types.callback_query,state: FSMContext):
    await state.finish()
    try:
        await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    except: pass

async def get_post(user_channel, message, state: FSMContext):
    await gener_post.step1.set()
    id_channel = return_chatid_channel(user_channel)  # ID Канала в который нужно отправить пост
    await state.update_data(idchannel=id_channel)
    await state.update_data(a=0)
    markup3 = types.InlineKeyboardMarkup()
    bat1 = types.InlineKeyboardButton(text='Отмена', callback_data="cansel")
    markup3.add(bat1)
    go_text = await bot.send_message(message.chat.id, text=f"""Вы выбрали канал <b>@{user_channel}</b> для создания поста.\n
<b>Сначала отправь медиафайл</b>, который будет использоваться в твоем посте""", parse_mode='html',reply_markup=markup3)
    await state.update_data(go_text=go_text.message_id)

    await state.update_data(user_channel777=user_channel,message777 = message, state777=state)


@dp.callback_query_handler(text='start_new', state="*")
async def start_new(call: types.callback_query,state: FSMContext):
    data = await state.get_data()
    mes1 = data['start_new1']
    mes2 = data['start_new2']
    await bot.delete_message(chat_id=call.message.chat.id,message_id=mes1.message_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=mes2.message_id)

    user_channel777 = data['user_channel777']
    message777 = data['message777']

    await get_post(user_channel=user_channel777,message=message777,state=state)






########## ОТПРАВКА ПОСТА В КАНАЛ
@dp.callback_query_handler(text='send_post', state='*')
async def send_post(call: types.callback_query, state: FSMContext):
    await bot.send_message(chat_id=call.message.chat.id,text='<b>Пост опубликован!</b>\n\n'
                                                             'Создать новый - /post',parse_mode='html')

    data = await state.get_data()
    id_channel = data['idchannel']
    send_message = data['mes']
    try:
        a = data['markup']  # Cтарая клавиатура
    except: a=types.InlineKeyboardMarkup()
    id_messad = (await bot.copy_message(chat_id=id_channel, message_id=send_message.message_id, from_chat_id=call.message.chat.id,reply_markup=a)).message_id
    try:
        text_ok = data['text_ok']
        text_bad = data['text_bad']
        id_channel = id_channel
        id_user = call.message.chat.id

        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute(""" CREATE TABLE IF NOT EXISTS user_bat(
               id_messad,
               text_ok,
               text_bad,
               id_channel,
               id_user
               ) """)
        db.commit()

        sql.execute(f"INSERT INTO user_bat VALUES (?,?,?,?,?)", (id_messad,text_ok,text_bad,id_channel,id_user))
        db.commit()
    except: pass
    id_del1 = data['start_new2']
    id_del2 = data['start_new1']

    try:
        await bot.delete_message(chat_id=call.message.chat.id,message_id=id_del1.message_id)
    except:
        pass
    try:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=id_del2.message_id)
    except: pass
    await state.finish()

############


@dp.message_handler(state=gener_post.step1, content_types=['photo', 'video'])
async def name_channel(message: types.Message, state: FSMContext):
    # Предосмотр поста
    go_photo = await bot.copy_message(chat_id=message.chat.id, message_id=message.message_id,
                                      from_chat_id=message.chat.id)

    # Сообщение о предосмотре поста
    del_mes = await bot.send_message(chat_id=message.chat.id,
                                     text=f"👆Сейчас твой пост выглядит так\n\nТеперь <b>отправь текст</b>, который ты хочешь прикрепить к своему посту\n\n"
                                          f"<i>Ты можешь использовать разметку html</i>",
                                     reply_markup=markup, parse_mode='html')

    # Обновление сета
    await state.update_data(go_photo=go_photo)  # Занесение в сет медиафайл
    await state.update_data(mes=go_photo)  # Занесение в сет медиафайл
    await state.update_data(del_mes=del_mes)  # Занесение в сет Сообщения о предосмотре
    await state.update_data(start_new1=del_mes)  # Занесение в сет Сообщения о предосмотре
    await state.update_data(start_new2=go_photo)  # Занесение в сет Сообщения о предосмотре

    # Читска
    a = (await state.get_data())['go_text']  # Читка
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Чистка
    await bot.delete_message(chat_id=message.chat.id, message_id=a)  # Чистка

    # Регистрация следующего шага
    await gener_post.step2.set()


@dp.message_handler(state=gener_post.step2, content_types='text')
async def name_step2(message: types.Message, state: FSMContext):
    # Предосмотр поста
    a = (await state.get_data())['go_photo']  # Получение медиафайла
    go_photo2 = await bot.copy_message(chat_id=message.chat.id, message_id=a.message_id, from_chat_id=message.chat.id,caption=message.text,parse_mode='html')
    await state.update_data(mes=go_photo2)
    # Сообщение о предосмотре поста
    del_mes2 = await bot.send_message(chat_id=message.chat.id, text=text_but, reply_markup=markup2,parse_mode='html')  # Сообщение про то, как нужно добавлять кнопки

    # Обновление сета
    await state.update_data(start_new1=go_photo2)  # Занесение в сет Сообщения о предосмотре
    await state.update_data(start_new2=del_mes2)  # Занесение в сет Сообщения о предосмотре

    await state.update_data(go_photo2=go_photo2)  # Занесение в сет медиафайла с текстом
    await state.update_data(del_mes2=del_mes2)  # Занесение в сет Сообщения о предосмотре
    await state.update_data(key=0)  # Занесение в сет Сообщения о предосмотре

    # Читска
    a = (await state.get_data())['del_mes']  # Читка старого предосмотра
    await bot.delete_message(chat_id=message.chat.id, message_id=a.message_id)
    b = (await state.get_data())['go_photo']  # Читка старого медиафайла
    await bot.delete_message(chat_id=message.chat.id, message_id=b.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)  # Чистка только что отправленного сообщения

    # Регистрация следующего шага
    await gener_post.step3.set()


@dp.message_handler(content_types='text', state=gener_post.step3)
async def add_button(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.chat.id, message_id=call.message_id)
    try:
        if ((await state.get_data())['key']) == 0:  # Первый раз отправил кнопку:
            a = optioon_but(call.text)
            mes_photo = ((await state.get_data())['go_photo2'])  # Cтарое сообщение с фото

            # генерация клавиатуры
            markup = types.InlineKeyboardMarkup()

            if len(a) == 1:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                markup.add(bat1)

            elif len(a) == 2:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                bat2 = types.InlineKeyboardButton(text=a[1]['name'], url=a[1]['url'])
                markup.add(bat1, bat2)

            elif len(a) == 3:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                bat2 = types.InlineKeyboardButton(text=a[1]['name'], url=a[1]['url'])
                bat3 = types.InlineKeyboardButton(text=a[2]['name'], url=a[2]['url'])
                markup.add(bat1, bat2, bat3)

            else:
                await bot.send_message(chat_id=call.chat.id, text='Вы ввели неверный формат кнопок')
            # генерация клавиатуры

            mes = await bot.copy_message(chat_id=call.chat.id, from_chat_id=call.chat.id,
                                         message_id=mes_photo.message_id, reply_markup=markup)
            mes1 = await bot.send_message(chat_id=call.chat.id, text='Сейчас твой пост выглядит так\n\n'
                                                                     'Жми <b>ДАЛЕЕ</b>, если закончил добавление URL Кнопок\n\n'
                                                                     'Ты <b>можешь продолжать</b> отправлять кнопки в том же формате, что бы добавить еще одну строку кнопок',
                                          reply_markup=markup2, parse_mode='html')

            await state.update_data(start_new1=mes)  # Занесение в сет Сообщения о предосмотре
            await state.update_data(start_new2=mes1)  # Занесение в сет Сообщения о предосмотре
            await state.update_data(markup=markup)
            await state.update_data(mes=mes)
            await bot.delete_message(chat_id=call.chat.id, message_id=mes_photo.message_id)

            try:
                a = (await state.get_data())['del_mes2']  # Читка старого предосмотра
                await bot.delete_message(chat_id=call.chat.id, message_id=a.message_id)
                b = (await state.get_data())['go_photo2']  # Читка старого медиафайла
                await bot.delete_message(chat_id=call.chat.id, message_id=b.message_id)

            except:
                pass  # Очистка предыдущий сообщений
            await state.update_data(key=1)

        else:  # Отправляет кнопки второй и последующий раз
            markup = ((await state.get_data())['markup'])  # Cтарая клавиатура
            a = optioon_but(call.text)

            if len(a) == 1:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                markup.add(bat1)

            elif len(a) == 2:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                bat2 = types.InlineKeyboardButton(text=a[1]['name'], url=a[1]['url'])
                markup.add(bat1, bat2)

            elif len(a) == 3:
                bat1 = types.InlineKeyboardButton(text=a[0]['name'], url=a[0]['url'])
                bat2 = types.InlineKeyboardButton(text=a[1]['name'], url=a[1]['url'])
                bat3 = types.InlineKeyboardButton(text=a[2]['name'], url=a[2]['url'])
                markup.add(bat1, bat2, bat3)

            await state.update_data(markup=markup)
            a = (await state.get_data())['mes']
            b = await bot.edit_message_reply_markup(chat_id=call.chat.id, message_id=a.message_id, reply_markup=markup)
            await state.update_data(start_new1=b)  # Занесение в сет Сообщения о предосмотре
            await state.update_data(mes=b)

            try:
                # Чистка
                a = (await state.get_data())['del_mes2']  # Читка старого предосмотра
                await bot.delete_message(chat_id=call.chat.id, message_id=a.message_id)
                b = (await state.get_data())['go_photo2']  # Читка старого медиафайла
                await bot.delete_message(chat_id=call.chat.id, message_id=b.message_id)
            except:
                pass



    except:
        await bot.send_message(call.chat.id, text='Вводите пожалуйста кнопки в нашем формате!')


@dp.callback_query_handler(text='create_dable', state='*')
async def create_dable_but(call: types.callback_query, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, text=text_but2, message_id=call.message.message_id,parse_mode='html',reply_markup=markup3)
    await gener_post.step4.set()


@dp.message_handler(content_types='text', state=gener_post.step4)
async def add_button2(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.chat.id, message_id=call.message_id)
    d = optioon_duble_button(call.text)
    if len(d) != 3:
        await bot.send_message(chat_id=call.chat.id, text='Неверный формат')
    else:
        try:
            a = (await state.get_data())['markup']  # Cтарая клавиатура
        except:
            a = types.InlineKeyboardMarkup()
        mes = (await state.get_data())['mes']  # Сообщение с картинкой и тестом

        data = await state.get_data()
        id_channel = data['idchannel']

        # Генерация новой клавиатуры
        ##### ОЩИБКА В ТОМ ЧТО В КАЛЛБЕК ДАТЕ НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ много символов
        bat1 = types.InlineKeyboardButton(text=d[0], callback_data=f'tap_dable+{id_channel}')
        a.add(bat1)


        await state.update_data(markup=a)

        await state.update_data(text_bad=d[1])
        await state.update_data(text_ok=d[2])



        await bot.edit_message_reply_markup(chat_id=call.chat.id,message_id=mes.message_id,reply_markup=a)


        await state.update_data(start_new1=mes)  # Занесение в сет Сообщения о предосмотре


@dp.callback_query_handler(text='create_reak', state='*')
async def create_reak_but(call: types.callback_query, state: FSMContext):
    data = await state.get_data()
    mes1 = data['start_new2']
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=mes1.message_id,text=text_but3,parse_mode='html',reply_markup=markup)
    await gener_post.step5.set()


@dp.message_handler(content_types='text', state=gener_post.step5)
async def add_button3(message: types.Message, state: FSMContext):
    print(message)
    text = message.text
    arr = text.split('-')
    if len(arr) == 2 or len(arr) == 1:
        dannie = arr
        k = -1
        for i in arr:
            k += 1
            if i[0] == ' ':
                if i[-1] == ' ':
                    dannie[k] = (i[1:-1])
                else:
                    dannie[k] = (i[1:])

            else:
                if i[-1] == ' ':
                    dannie[k] = (i[:-1])
                else:
                    pass
        if len(dannie) == 2:
            if (len(dannie[0]) != 1 or len(dannie[1]) != 1):
                await bot.send_message(chat_id=message.chat.id, text='<b>Используй только два смайла в формате:</b>.'
                                                                     '👍 - 👎', parse_mode='html')
            else:
                try:
                    a = (await state.get_data())['markup']  # Cтарая клавиатура
                except:
                    a = types.InlineKeyboardMarkup()

                batq1 = types.InlineKeyboardButton(text=f'{dannie[0]}0',
                                                   callback_data=f'reakch{dannie[0]}')  # ОБРАБОТАТЬ НАЖАТИЕ НА КНОПКУ
                batq2 = types.InlineKeyboardButton(text=f'{dannie[1]}0',
                                                   callback_data=f'reakch{dannie[1]}')  # ОБРАБОТАТЬ НАЖАТИЕ НА КНОПКУ
                a.add(batq1, batq2)
                await state.update_data(markup=a)
                mes = (await state.get_data())['mes']  # Сообщение с картинкой и тестом
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=mes.message_id, reply_markup=a)
        else:
            if len(dannie[0]) != 1:
                await bot.send_message(chat_id=message.chat.id,
                                       text='<b>Отправь мне либо только однин смайл или два смайла в формате:</b>'
                                            '👍 - 👎', parse_mode='html')
            else:
                try:
                    a = (await state.get_data())['markup']  # Cтарая клавиатура
                except:
                    a = types.InlineKeyboardMarkup()

                batq1 = types.InlineKeyboardButton(text=f'{dannie[0]}0',
                                                   callback_data=f'reakch{dannie[0]}')  # ОБРАБОТАТЬ НАЖАТИЕ НА КНОПКУ
                a.add(batq1)
                await state.update_data(markup=a)
                mes = (await state.get_data())['mes']  # Сообщение с картинкой и тестом
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=mes.message_id, reply_markup=a)




    else:
        await bot.send_message(chat_id=message.chat.id, text="<b>Вводи кнопки в формате:</b>\n"
                                                             "👍 - 👎", parse_mode='html')


@dp.callback_query_handler(text_startswith= 'reakch', state='*')
async def dfldsfk (call : types.callback_query, state: FSMContext):
    try:
        q =(call.data[6:])
        a = (call.message.reply_markup['inline_keyboard'])
        ks = -1
        n=0
        k = -1 # Номер строчки в которой находится наша кнопка
        for i in a:# Перебирает строчки клавы
            if len(i) == 2:
                n+=1
            k+=1
            for ii in i: #Перебирает значения в строчке
                ks+=1
                if q in ii['text'] and (ii['text'][1] in '0123456789'):
                    if q in i[0]['text']:
                        text = call.message.reply_markup['inline_keyboard'][int(k)][int(0)]['text']
                        text1 = text[0]
                        text2 = int(text[1:])
                        call.message.reply_markup['inline_keyboard'][int(k)][int(0)]['text'] = f'{text1}{text2+1}'
                        new_markup = call.message.reply_markup
                        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=new_markup)
                        break
                    elif q in i[1]['text']:
                        text = call.message.reply_markup['inline_keyboard'][int(k)][int(1)]['text']
                        text1 = text[0]
                        text2 = int(text[1:])
                        call.message.reply_markup['inline_keyboard'][int(k)][int(1)]['text'] = f'{text1}{text2 + 1}'
                        new_markup = call.message.reply_markup
                        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                            message_id=call.message.message_id, reply_markup=new_markup)
                        break


    except:pass

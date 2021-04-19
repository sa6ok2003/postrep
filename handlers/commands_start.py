from aiogram import types
from misc import dp,bot
from .sqlit import reg_user

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    print(message)
    reg_user(message.chat.id)
    await bot.send_message(message.chat.id, 'Я помогу тебе создавать посты в Telegram каналы, прикреплять фото, видео, кнопки и многое другое!\n\n'
                                            '<b>/addchannel - добавить канал\n'
                                            '/post -  создать пост</b>\n\n'
                                            'Инструкция : @InfoBotPost',parse_mode='html')
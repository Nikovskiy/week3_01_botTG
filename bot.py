import logging

import pandas as pd
import numpy as np
import string
import os 

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command



TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("Токен не найден! Укажите переменную окружения TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename='log.txt')


@dp.message(Command(commands=['start']))
async def process_command_start(message:Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!!! Я — бот, который занимается транслитерацией с русского языка. Напиши мне что-нибудь на русском, и я обязательно латинизирую.'
    logging.info(f'{user_name}{user_id} started bot')
    await bot.send_message(chat_id=user_id, text=text)


@dp.message()
async def process_rus_to_latin(message:Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    table = pd.read_excel('rus_to_latin.xlsx', engine='openpyxl')
    text = ''
    punc = string.punctuation + ' '

    for i in message.text:
        try:
            if i not in punc:
                row = table[table['Национальный знак'] == i.upper()]
                char = row['Рекомендуемая транслитерация'].values[0]
                if i.islower():
                    text += char.lower()
                else:
                    text += char
            else:
                text += i
        except:
            continue
    
    logging.info(f'{user_name}{user_id} translated text {text}: length {len(text)}')
    await bot.send_message(chat_id=user_id, text=text)#bot.send_message(chat_id=user_id, text=text)

if __name__ == '__main__':
    dp.run_polling(bot)

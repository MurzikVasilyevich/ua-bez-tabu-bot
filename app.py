import os

from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import pandas as pd

df = pd.read_csv('data.csv')
bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN'])

terms = [['💋', '🍆', '🌮', '🍑🍆', '🌰'], ['( • )( • )', '🥚🥚', '🍑', '👉👌', '👉👌👈']]
markup = types.ReplyKeyboardMarkup()
# loop enumerate terms
for rows in terms:
    row = [types.KeyboardButton(x) for x in rows]
    markup.add(*row)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привіт! Я бот, який покаже вам наскільки різноманітною може бути Українська мова.
Натисніть на кнопку, аби подивитись синоніми.\
""", reply_markup=markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    df1 = df.loc[df['term'] == message.text]
    await bot.send_message(message.chat.id, df1.sample(1).iloc[0]['synonym'], reply_markup=markup)
    # await bot.reply_to(message, message.text, reply_markup=markup)


asyncio.run(bot.polling())

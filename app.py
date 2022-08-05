import logging.config
import os
import sys

from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import pandas as pd
import numpy as np

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app.py')


def main():
    logging.info("Starting main")

    url = "https://raw.githubusercontent.com/MurzikVasilyevich/ua-bez-tabu/main/synonyms.csv"
    df = pd.read_csv(url, index_col=0)
    bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN'])

    columns = 5
    terms = df['term_emoji'].dropna().unique()
    synonyms = df['synonym'].dropna().unique()
    terms_split = [list(i) for i in np.array_split(terms, columns)]
    markup = types.ReplyKeyboardMarkup(row_width=columns, resize_keyboard=True)
    # loop enumerate terms
    for rows in terms_split:
        row = [types.KeyboardButton(x) for x in rows]
        markup.add(*row)

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['about', 'start'])
    async def send_welcome(message):
        logging.info(f"Welcoming {message.chat.first_name} {message.chat.last_name} - {message.chat.username}")
        await bot.reply_to(message, """\
    Привіт! Я бот, який покаже вам наскільки різноманітною може бути Українська мова.
    Натисніть на кнопку, аби подивитись синоніми.\
    """, reply_markup=markup)

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda message: True)
    async def echo_message(message):
        logging.info(f"Echoing {message.chat.username} to {message.text}")
        if message.text in terms:
            await bot.reply_to(message,
                               df.loc[df['term_emoji'] == message.text].sample(1).iloc[0]['synonym'],
                               reply_markup=markup)
        elif message.text.lower() in list(synonyms):
            term = df.loc[df['synonym'] == message.text.lower()].iloc[0]['term']
            await bot.reply_to(message,
                               df.loc[df['term'] == term].sample(1).iloc[0]['synonym'],
                               reply_markup=markup)
        else:
            await bot.reply_to(message,
                               "Не знайдено такого синоніму. Спробуйте ще раз.")

    asyncio.run(bot.infinity_polling())


if __name__ == '__main__':
    sys.exit(main())

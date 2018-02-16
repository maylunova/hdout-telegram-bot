# A telegram bot for tracking new episodes of TV series on HDOut.TV

from datetime import datetime, timedelta
import logging

import feedparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
from constants import GREETING, BASE_URL


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log')

delta = timedelta(days=1)

def  greet_user(bot, update):
    # TODO проверяем наличие id в БД, если нет - приетствие с инструкцией, если да -  другое приветствие
    update.message.reply_text(GREETING)


def get_user_id(bot, update):
    user_text = update.message.text
    logging.info(user_text)
    whats_news(bot, update, user_id=user_text)


def whats_news(bot, update, user_id):
    rss = '{}{}/'.format(BASE_URL, user_id)
    # TODO обработка 404 и пустого rss
    favorite_series = feedparser.parse(rss)
    for series in favorite_series.entries:
        published_datetime = datetime.strptime(series.published, '%a, %d %b %Y %H:%M:%S %Z')
        tdelta = datetime.now() - published_datetime
        if tdelta <= delta:
            update.message.reply_text(series.published + '\n' + series.title + '\n' + series.link + '\n')


def main():
    updater = Updater(config.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, get_user_id))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

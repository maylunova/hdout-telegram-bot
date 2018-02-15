# A telegram bot for tracking new episodes of TV series on HDOut.TV

from datetime import datetime
import logging

import feedparser
from telegram.ext import Updater, CommandHandler

import config


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log')

delta = 1


def what_news(bot, update):
    favorite_series = feedparser.parse('https://hdout.tv/UserRSS/4064/')
    # print(type(favorite_series.entries[0]['published'])) =>> str Tue, 13 Feb 2018 20:57:49 UTC
    for series in favorite_series.entries:
        published_datetime = datetime.strptime(series.published, '%a, %d %b %Y %H:%M:%S %Z')
        tdelta = (datetime.today() - published_datetime).days
        if tdelta <= delta:
            update.message.reply_text(series.published + '\n' + series.title + '\n' + series.link + '\n')


def main():
    updater = Updater(config.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", what_news))

    updater.start_polling()
    updater.idle()


main()

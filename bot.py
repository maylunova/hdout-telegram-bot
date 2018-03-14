# A telegram bot for tracking new episodes of TV series on HDOut.TV
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
from constants import GREETING, ERROR_NO_DATA
from databases import add_to_db, check_db
from parser import parse_rss

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log')


def greet_user(bot, update):
    update.message.reply_text(GREETING)


def get_user_info(bot, update):
    user_text = update.message.text
    logging.info(user_text)
    episodes_list = parse_rss(hdout_id=user_text)
    if episodes_list is None:
        update.message.reply_text(ERROR_NO_DATA)
        update.message.reply_text(GREETING)
        return
    send_news(bot, update,
              hdout_id=user_text,
              episodes_list=episodes_list
              )


def send_news(bot, update, hdout_id, episodes_list):
    for epi in episodes_list:
        title = epi[0]
        sent = check_db(hdout_id=hdout_id, title=title)
        if sent is False:
            update.message.reply_text(epi[0] + '\n' + epi[1] + '\n' + epi[2] + '\n')
            add_to_db(hdout_id=hdout_id, title=title)


def main():
    updater = Updater(config.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, get_user_info))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# A telegram bot for tracking new episodes of TV series on HDOut.TV
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
from constants import GREETING, ERROR_NO_DATA
from databases import add_user_to_db, add_epi_to_db, check_db, User
from parser import parse_rss


def greet_user(bot, update):
    update.message.reply_text(GREETING)


def get_user_info(bot, update):
    chat_id = update.message.chat_id
    hdout_id = update.message.text
    logging.debug('User info for hdout_id: ' + str(hdout_id))
    check_user = parse_rss(hdout_id=hdout_id, delta=None)
    if check_user is None:
        update.message.reply_text(ERROR_NO_DATA)
        update.message.reply_text(GREETING)
        return
    user_id = add_user_to_db(chat_id=chat_id, hdout_id=hdout_id)
    send_news(bot, hdout_id, chat_id, user_id)


def update(bot, job):
    logging.debug('Update started')
    for user in User.query.all():
        hdout_id = user.hdout_id
        chat_id = user.chat_id
        user_id = user.id
        send_news(bot, hdout_id, chat_id, user_id)


def send_news(bot, hdout_id, chat_id, user_id):
    epis = parse_rss(hdout_id=hdout_id)
    for epi in epis:
        title = epi[0]
        sent = check_db(user_id=user_id, title=title)
        if sent is False:
            bot.sendMessage(chat_id=chat_id, text=epi[0] + '\n' + epi[1] + '\n' + epi[2] + '\n')
            add_epi_to_db(title=title, user_id=user_id)


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    updater = Updater(config.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, get_user_info))

    job_queue = updater.job_queue
    job_queue.run_repeating(update, interval=60*30)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
import feedparser
from pprint import pprint
import datetime
import random
import logging
import os

from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
                          Filters)

import core/db
import core/sources
import core/user
import core/quiz_builder

import cmd/start
import cmd/quiz
import cmd/help
import cmd/sources
import cmd/userinfo


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

                              
def main():
    logger.info("creating updater")
    updater = Updater(os.environ['TEL_BOT_TOKEN'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    
    dp.add_handler(CommandHandler('quiz', quiz))
    dp.add_handler(CommandHandler('q', quiz))
    dp.add_handler(CommandHandler('quiz3', lambda update,context: quiz(update, context, 3)))
    dp.add_handler(CommandHandler('q3', lambda update,context: quiz(update, context, 3)))
    dp.add_handler(CommandHandler('quiz4', lambda update,context: quiz(update, context, 4)))
    dp.add_handler(CommandHandler('q4', lambda update,context: quiz(update, context, 4)))
    dp.add_handler(PollHandler(receive_quiz_answer))
                              
    dp.add_handler(CommandHandler('help', help_handler))
    dp.add_handler(CommandHandler('h', help_handler))
    dp.add_handler(CommandHandler('short', short_handler))
    dp.add_handler(CommandHandler('credits', credits_handler))
    dp.add_handler(CommandHandler('qr', qr_handler))
    dp.add_handler(CommandHandler('sources', sources_handler))
    dp.add_handler(CommandHandler('userinfo', userinfo_handler))

    logger.info("starting to poll")
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print('Bot starting ...')
    main()

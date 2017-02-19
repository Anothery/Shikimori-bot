# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
from users import clear_state
from menu import main_menu
import answer_inspector


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@clear_state
def start(bot, update):
    bot.sendMessage(update.message.chat_id,
                    'Привет. Меня зовут Шикимори Бот!\n',)

    main_menu.menu(bot, update)


def main():
    token = 'YOUR_TOKEN'  # Токен бота
    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('menu', main_menu.menu))
    dp.add_handler(MessageHandler(Filters.text, answer_inspector.if_text))
    dp.add_handler(CallbackQueryHandler(answer_inspector.if_query))
    updater.start_polling()


if __name__ == '__main__':
    main()

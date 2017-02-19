# -*- coding: utf-8 -*-

from users import users
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shiki import Shiki


def rating_mode(bot, update, inline=False):
    chat_id = update.message.chat_id
    user_data = users[chat_id]['data']
    if user_data.get('page') is None or user_data.get('title') is None:
        user_data['page'] = 1
        user_data['title'] = ''  #
    page = user_data['page']
    title = user_data['title']
    api = Shiki()
    data = api.animes.search.get(page=page, q=title)
    prev = 'prev' if page > 1 else '-'
    next = '-' if not api.animes.search.get(page=page + 1, q=title) else 'next'

    menu_button = InlineKeyboardButton('В меню', callback_data='back')
    text = 'Аниме, отсортированные по рейтингу.\nСтраница %d' % page

    def getrating(api, id):
        return api.animes.get(str(id))['score']

    title_buttons = [[InlineKeyboardButton('({}) {}'.format(getrating(api, title['id']), title['russian'])
                                           , callback_data='id'+str(title['id']))] for title in data]
    title_buttons.append([InlineKeyboardButton('←', callback_data=prev),
                          menu_button,
                          InlineKeyboardButton('→', callback_data=next)])
    if inline:
        bot.editMessageText(chat_id=chat_id, message_id=update.message.message_id,
                            text=text,
                            reply_markup=InlineKeyboardMarkup(title_buttons))
    else:
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(title_buttons))
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from menu import search, main_menu, rating, calend
from users import users, if_new_user


# перехват текста
@if_new_user
def if_text(bot, update):
    if users[update.message.chat_id]['state'] == 'search':
        search.search_complete(bot, update)
    else:
        menu_button = [[InlineKeyboardButton('В меню', callback_data='back')]]
        update.message.reply_text('Непонятная команда.\n',
                                  reply_markup=InlineKeyboardMarkup(menu_button))


# перехват запросов
def if_query(bot, update):
    query = update.callback_query
    # main menu
    if query.data == 'search':
        search.search_start(bot, query)
    if query.data == 'rating':
        users[query.message.chat_id]['state'] = 'rating'
        rating.rating_mode(bot, query)
    if query.data == 'calendar':
        calend.calendar(bot, query)

    # search menu
    elif query.data == 'prev':
        try:
            users[query.message.chat_id]['data']['page'] -= 1
            if users[query.message.chat_id]['state'] == 'rating':
                rating.rating_mode(bot, query, True)
            else:
                search.search_complete(bot, query, True)
        except:
            obsolete(bot, query)
    elif query.data == 'next':
        try:
            users[query.message.chat_id]['data']['page'] += 1
            if users[query.message.chat_id]['state'] == 'rating':
                rating.rating_mode(bot, query, True)
            else:
                search.search_complete(bot, query, True)
        except:
            obsolete(bot, query)
    elif query.data == 'back':
        main_menu.menu(bot, query)
    elif query.data[:2] == 'id':
            search.show_info(bot, query)
    elif query.data == 'back_to_list':
        try:
            if users[query.message.chat_id]['state'] == 'rating':
                rating.rating_mode(bot, query)
            else:
                search.search_complete(bot, query)
        except:
            obsolete(bot, query)
    elif query.data[:4] == 'date':
        calend.show(bot, query)
    elif query.data == 'back_to_calend':
        calend.calendar(bot, query)


def obsolete(bot, query):
    bot.editMessageText(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Ошибка! Это сообщение устарело\nВернитесь в меню и попробуйте снова!')


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False



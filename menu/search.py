from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from users import users, clear_state
from shiki import Shiki
import re


@clear_state
def search_start(bot, query):
    bot.editMessageText(text='Поиск по аниме.\nВведите название:',
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id )
    users[query.message.chat_id]['state'] = 'search'


def search_complete(bot, update, inline=False):
    chat_id = update.message.chat_id
    user_data = users[chat_id]['data']
    #  При первом вводе
    if user_data.get('page') is None or user_data.get('title') is None:
        user_data['page'] = 1
        user_data['title'] = update.message.text
    page = user_data['page']
    title = user_data['title']
    menu_button = InlineKeyboardButton('В меню', callback_data='back')
    api = Shiki()
    data = api.animes.search.get(page=page, q=title)

    if not data:
        update.message.reply_text('Увы, по запросу %s ничего не найдено' % update.message.text,
                                  reply_markup=InlineKeyboardMarkup([[menu_button]]))
    else:
        text = 'Результат поиска по запросу: %s\nСтраница: %d' % (title, page)
        prev = 'prev' if page > 1 else '-'
        next = '-' if not api.animes.search.get(page=page+1, q=title) else 'next'
        title_buttons = [[InlineKeyboardButton(title['russian'], callback_data='id'+str(title['id']))] for title in data]

        title_buttons.append([InlineKeyboardButton('←', callback_data=prev),
                              menu_button,
                              InlineKeyboardButton('→', callback_data=next)])
        if inline:
            bot.editMessageText(chat_id=chat_id, message_id=update.message.message_id,
                                text=text,
                                reply_markup=InlineKeyboardMarkup(title_buttons))
        else:
            update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(title_buttons))

    users[chat_id]['state'] = '-'


def show_info(bot, query):
    api = Shiki()
    data = api.animes.get(query.data[2:])
    status = {'released':'вышедшее', 'latest': 'недавно вышедшее',
              'ongoing': 'сейчас выходит', 'anons': 'анонсировано'}
    genres = ''
    for genre in data['genres']:
        genres += genre['russian'] + ' '
    text = 'Название: {} ({})\n' \
           'Статус: {}\n' \
           'Жанр: {}' \
           'Рейтинг: {}\n' \
           'Количество эпизодов: {}\n' \
           'Дата выхода: {}\n' \
           'Смотреть на сайте: shikimori.org{}\n' \
           'Описание: {}'.format(data['russian'],
                                 data['name'],
                                 status[data['status']],
                                 genres,
                                 data['score'],
                                 data['episodes'],
                                 data['aired_on'],
                                 data['url'],
                                 'нет' if not data['description']
                                            else re.sub(r'\[[^\]]+\]', '', data['description']))

    back_button = [InlineKeyboardButton('Назад ↺', callback_data='back_to_list')]
    bot.sendPhoto(chat_id=query.message.chat_id, photo='https://shikimori.org{}'.format(data['image']['original']))
    query.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup([back_button]))


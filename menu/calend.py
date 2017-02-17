from shiki import Shiki
from datetime import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def calendar(bot, update):
    api = Shiki()
    data = api.calendar.get()
    date = []
    month = [None, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля'
        , 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    for title in data:
        if not (title['next_episode_at'][:10] in date):
            date.append(title['next_episode_at'][:10])
        if len(date) == 7: break
    calendar_buttons = []
    for time in date:
        temp = datetime.strptime(time, '%Y-%m-%d')
        text = '%d %s\n' % (temp.day, month[temp.month])
        callback = 'date' + time
        calendar_buttons.append([InlineKeyboardButton(text, callback_data=callback)])
    calendar_buttons.append([InlineKeyboardButton('В меню', callback_data='back')])
    update.message.reply_text('Календарь на 7 дней', reply_markup=InlineKeyboardMarkup(calendar_buttons))


def show(bot, update):
    date = update.data[4:]
    temp = datetime.strptime(date, '%Y-%m-%d')
    api = Shiki()
    data = api.calendar.get()
    month = [None, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля'
            , 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    text = '%d %s\n' %(temp.day, month[temp.month])
    for title in data:
        if title['next_episode_at'][:10] == date:
            text += "\n[Эпизод %s]\n%s\n(%s)\n—" % (title['next_episode'],
                                                   title['anime']['russian'],
                                                   title['anime']['name'])

    back_button = [InlineKeyboardButton('Назад ↺', callback_data='back_to_calend')]
    bot.editMessageText(chat_id=update.message.chat_id,
                        message_id=update.message.message_id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup([back_button])
                       )

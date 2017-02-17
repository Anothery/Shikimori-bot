from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from users import clear_state


@clear_state
def menu(bot, update):  # main menu

    search_button = [InlineKeyboardButton('Найти аниме', callback_data='search')]
    rating_button = [InlineKeyboardButton('Рейтинг аниме', callback_data='rating')]
    calendar_button = [InlineKeyboardButton('Календарь', callback_data='calendar')]

    main_menu = [search_button,
                 rating_button,
                 calendar_button]
    update.message.reply_text('Меню', reply_markup=InlineKeyboardMarkup(main_menu))


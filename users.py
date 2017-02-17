
# словарь всех текущих пользователей id : {состояние, {данные}}
users = dict()


# проверка на вхождение пользователя в словарь
def in_users(chat_id):
    if chat_id in users:
        return True
    else:
        return False


#  если пользователя нет в списке добавляем его
def if_new_user(function):
    def new(bot, update):
        if not in_users(update.message.chat_id):
            # состояние '-' если пользователь не предпринимает действий
            users[update.message.chat_id] = {'state': '-', 'data': {}}
        function(bot, update)
    return new


#  декоратор для очистки временных данных пользователя при переходе в меню
def clear_state(function):
    def clear(bot, update):
        if in_users(update.message.chat_id):
            users[update.message.chat_id]['state'] = '-'
            users[update.message.chat_id]['data'].clear()
        else:
            users[update.message.chat_id] = {'state': '-', 'data': {}}
        function(bot, update)
    return clear

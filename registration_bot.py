import telebot
from telebot import types
from string import Template

import config


bot = telebot.TeleBot(config.TOKEN)


user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'site']

        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/site')
    itembtn2 = types.KeyboardButton('/about')
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, f'Здравствуйте, '
                                      f'{message.from_user.first_name}, '
                                      f'чем вам помочь?', reply_markup=markup)


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, 'Мы компания Vies.Tech.'
                                      'Мы занимаемся WEB-разработкой под ключ: '
                                      'разработка сайтов, приложений, CRM-систем')


@bot.message_handler(commands=['site'])
def choice_city(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Краснодар')
    itembtn2 = types.KeyboardButton('Москва')
    itembtn3 = types.KeyboardButton('Санкт-Петербург')
    itembtn4 = types.KeyboardButton('Сочи')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    msg = bot.send_message(message.chat.id, 'Выберите ваш город?', reply_markup=markup)
    bot.register_next_step_handler(msg, get_username)


def get_username(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Фамилия Имя Отчество:', reply_markup=markup)
        bot.register_next_step_handler(msg, get_user_number)

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так!')


def get_user_number(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефона:')
        bot.register_next_step_handler(msg, choice_site)

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так!')


def choice_site(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Лендинг')
        itembtn2 = types.KeyboardButton('Многостраничник')
        itembtn3 = types.KeyboardButton('CRM-система')
        itembtn4 = types.KeyboardButton('Одностраничник')

        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(chat_id, 'Какой сайт вы хотите?', reply_markup=markup)
        bot.register_next_step_handler(msg, registration)

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так!')


def registration(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.site = message.text

        # показ сформированной заявки пользователю
        bot.send_message(chat_id, get_registration_data(user, 'Ваша заявка,', message.from_user.first_name),
                         parse_mode="Markdown")

        # отправить в группу
        bot.send_message(config.CHAT_ID, get_registration_data(user, 'Заявка от бота,', bot.get_me().username),
                         parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так!')


def get_registration_data(user, title, name):
    return f'Ваша заявка, {name}\n Город: {user.city}\n ФИО: {user.fullname}\n ' \
           f'Телефон: {user.phone}\n Выбранный сайт: {user.site}'


if __name__ == '__main__':
    bot.polling(none_stop=True)



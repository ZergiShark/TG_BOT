import telebot

import db

import utils

bot = telebot.TeleBot('5144984252:AAHV7RABQQfS_fwqAHFZacaghAco_opHKBE', parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    db.create_client(message.from_user.id, message.from_user.first_name)
    bot.send_message(message.chat.id, 'Привет! Я бот! Нажми /menu чтоб получить меню', )


@bot.message_handler(commands=['menu'])
def send_menu(message):
    bot.send_message(message.chat.id, 'Выберите пиццу:', reply_markup=utils.create_menu())


@bot.callback_query_handler(func=lambda call: True)
def add_position(call):
    db.create_basket_item(call.from_user.id, call.data)
    bot.send_message(call.from_user.id, 'Добавлено в корзину', )


bot.infinity_polling()

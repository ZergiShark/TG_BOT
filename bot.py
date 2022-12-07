import telebot
from telebot import types

import db

import utils

bot = telebot.TeleBot('5144984252:AAHV7RABQQfS_fwqAHFZacaghAco_opHKBE')

def main_markup():
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('Меню'), types.KeyboardButton('Корзина'))
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    db.create_client(message.from_user.id, message.from_user.first_name)
    bot.send_message(message.chat.id, 'Привет! Я бот! Нажми /menu чтоб получить меню', reply_markup=main_markup())


@bot.message_handler(content_types=['text'])
def keyboard_handler(message):
    if message.text == 'Меню':
        bot.send_message(message.chat.id, 'Выберите позицию:', reply_markup=utils.create_menu())
    elif message.text == 'Корзина':
        bot.send_message(message.chat.id, utils.get_basket(message.chat.id))
    # elif message.text == 'Оформить заказ':
    #     bot.send_message(message.chat.id, 'Ваши товары в корзине', utils.create_menu())


#Inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def add_position(call):
    db.create_basket_item(call.from_user.id, call.data)
    bot.send_message(call.from_user.id, 'Добавлено в корзину', )


bot.infinity_polling()

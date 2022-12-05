from telebot import types

from models import Position


def create_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for position in Position.all():
        buttons.append(types.InlineKeyboardButton(
            f"{position.title} - {position.price} рублей", callback_data=position.id
        ))
    markup.add(*buttons)
    return markup



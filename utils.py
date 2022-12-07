from telebot import types

from TG_BOT.db import get_client, get_positions
from models import Position, BasketItem


def create_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for position in Position.all():
        buttons.append(types.InlineKeyboardButton(
            f"{position.title} - {position.price} рублей", callback_data=position.id
        ))
    markup.add(*buttons)
    return markup


def get_basket(telegram_id):
    position_name = ['Ваши товары в магазине:', '']
    positions = get_positions(telegram_id)
    total_price = 0
    for position in positions:
        position_name.append(f'{position.title} x 1 - {position.price}')
        total_price += position.price
    position_name.append('')
    position_name.append("ИТОГО: " + str(total_price))
    return '\n'.join(position_name)




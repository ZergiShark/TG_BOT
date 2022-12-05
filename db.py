from typing import Optional
from models import Client, DBModel, Position, BasketItem


def get_client(telegram_id):
    for client in Client.filter(telegram_id=telegram_id):
        return client

def create_client(telegram_id, name):
    client = get_client(telegram_id)
    if client is None:
        client = Client(telegram_id=telegram_id, name=name)
        client.save()
    return client

def create_basket_item(telegram_id, position_id):
    client = get_client(telegram_id)
    basket = BasketItem(client_id=client.id, position_id = position_id)
    basket.save()
    return basket
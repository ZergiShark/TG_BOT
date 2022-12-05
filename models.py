from abc import ABC
import dataclasses
import sqlite3


class DBModel(ABC):
    @staticmethod
    def get_filter_query(data):
        result = []
        for field, value in data.items():
            if isinstance(value, str):
                result.append(f"{field}=='{value}'")
            else:
                result.append(f"{field}=={value}")
        return " AND ".join(result)

    @classmethod
    def all(cls):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        fields = ", ".join(cls.__annotations__)
        data = cursor.execute(f"SELECT {fields} FROM {cls.Meta.table_name};").fetchall()
        return [cls(*item) for item in data]

    @classmethod
    def filter(cls, **kwargs):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        fields = ", ".join(cls.__annotations__)
        query = cls.get_filter_query(kwargs)
        data = cursor.execute(f"SELECT {fields} FROM {cls.Meta.table_name} WHERE {query};").fetchall()
        return [cls(*item) for item in data]  # генератор списков python

    @classmethod
    def get(cls, pk):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        fields = ", ".join(cls.__annotations__)
        data = cursor.execute(f"SELECT {fields} FROM {cls.Meta.table_name} WHERE id=={pk};").fetchone()
        if data:
            return cls(*data)

    @staticmethod
    def get_set_query(data):
        new = []
        for field, value in data.items():
            if isinstance(value, str):
                new.append(f"{field}='{value}'")
            else:
                new.append(f"{field}={value}")
        return ", ".join(new)

    def save(self):
        base = sqlite3.connect("data.db")
        cursor = base.cursor()
        if self.id is None:
            fields = self.__dict__.copy()
            fields.pop("id")
            name_table = self.Meta.table_name
            keys_fields = ', '.join(fields.keys())
            values_fields = ', '.join('?' * len(fields))
            data = cursor.execute(f"INSERT INTO {name_table} ({keys_fields}) VALUES ({values_fields})", tuple(fields.values()))
            base.commit()
            self.id = data.lastrowid
        else:
            fields = self.__dict__.copy()
            fields.pop("id")
            cursor.execute(f"UPDATE {self.Meta.table_name} SET {self.get_set_query(fields)} WHERE id=={self.id}")
            base.commit()

    class Meta:
        table_name = None


# ORM - object relation mapping (сопоставление связанных объектов)
@dataclasses.dataclass
class Position(DBModel):
    title: str
    price: int
    weight: int
    description: str
    image: str
    id: int = None

    class Meta:
        table_name = "positions"



@dataclasses.dataclass
class Client(DBModel):
    telegram_id: int
    name: str
    id: int = None


    class Meta:
        table_name = "clients"


@dataclasses.dataclass
class Order(DBModel):
    id: int
    created_at: int
    status: str
    amount: int
    client_id: int

    class Meta:
        table_name = "orders"


@dataclasses.dataclass
class OrderItem(DBModel):
    id: int
    order_id: int
    position_id: int

    class Meta:
        table_name = "order_items"


@dataclasses.dataclass
class BasketItem(DBModel):
    client_id: int
    position_id: int
    id: int = None

    class Meta:
        table_name = "basket_items"
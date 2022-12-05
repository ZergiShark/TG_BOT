import sqlite3

base = sqlite3.connect("data.db")
cur = base.cursor()

position_table = [{
    "id": "1",
    "title": "Пицца маргарита",
    "price": "350",
    "weight": "500",
    "description": "Класическая пицца на тонком тесте",
    "image": "https://avatars.dzeninfra.ru/get-zen_doc/4340095/pub_60b21ce2131e0811903ba783_60b21d271e59e701157d4a28/scale_1200"}
    ,{
    "id": "2",
    "title": "Пицца пеперони",
    "price": "500",
    "weight": "500",
    "description": "Пицца пеперони на тонком тесте",
    "image": "https://musafir-edanadom.ru/wp-content/uploads/2022/06/piczcza-pepperoni-zakazat.jpg"},
    {
    "id": "3",
    "title": "Пицца гавайская",
    "price": "450",
    "weight": "500",
    "description": "Любимая всеми гавайская пицца",
    "image": "https://www.koolinar.ru/all_image/recipes/156/156543/recipe_7b4bb7f7-1d42-428a-bb0a-3db8df03093a.jpg"
}]

base.execute(
    "CREATE TABLE IF NOT EXISTS positions("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "title CHAR(255),"
    "price INTEGER,"
    "weight INTEGER,"
    "description TEXT,"
    "image CHAR(511));"
)
base.commit()

base.execute(
    "CREATE TABLE IF NOT EXISTS clients("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "telegram_id INT UNIQ,"
    "name CHAR(255));"
)
base.commit()

base.execute(
    "CREATE TABLE IF NOT EXISTS orders("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "created_at INT,"
    "status CHAR(255),"
    "amount INTEGER,"
    "client_id INTEGER,"
    "FOREIGN KEY(client_id) REFERENCES clients(id));"
)
base.commit()

base.execute(
    "CREATE TABLE IF NOT EXISTS order_items("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "order_id INTEGER,"
    "position_id INTEGER,"
    "FOREIGN KEY(position_id) REFERENCES positions(id),"
    "FOREIGN KEY(order_id) REFERENCES orders(id));"
)
base.commit()

base.execute(
    "CREATE TABLE IF NOT EXISTS basket_items("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "client_id INTEGER,"
    "position_id INTEGER,"    
    "FOREIGN KEY(client_id) REFERENCES clients(id),"
    "FOREIGN KEY(position_id) REFERENCES positions(id));"
)
base.commit()

for item in position_table:
    cur.execute("INSERT INTO positions VALUES(?, ?, ?, ?, ?, ?)", (tuple(item.values())))
    base.commit()
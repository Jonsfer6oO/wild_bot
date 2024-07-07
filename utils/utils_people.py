import sqlite3

#добавление нового пользователя
def new_people(id, username, money,attems,count_attems, time = 30):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS people(
                   id INTEGER,
                   username TEXT,
                   money INTEGER,
                   attems INTEGER,
                   count_attems INTEGER,
                   time INTEGER
                   )""")

    cursor.execute("INSERT INTO people VALUES(?, ?, ?, ?, ?, ?);", (id, username, money,attems,count_attems, time))

    conn.commit()
    conn.close

# проверка пользователя на наличие в базе данных
def check_people():
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people")
    user_id = list(cursor.fetchall())

    conn.close()

    return [int(i[0]) for i in user_id]


# смена времени
def update_time(id, time):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people SET time = ? WHERE id = ?", (time, id))

    conn.commit()
    conn.close()

#данные пользователя
def list_str_people(id):
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people")
    user_id = list(cursor.fetchall())

    conn.close()

    for i in user_id:
        if i[0] == id:
            return list(i)

# смена количества денег
def update_money(id, money):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people SET money = ? WHERE id = ?", (money, id))

    conn.commit()
    conn.close()

# смена количества опросов
def update_attems(id, count_poll):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people SET count_attems = ? WHERE id = ?", (count_poll, id))

    conn.commit()
    conn.close()

# выход из панели заказчика
def update_exit(id, status):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people SET attems = ? WHERE id = ?", (status, id))

    conn.commit()
    conn.close()

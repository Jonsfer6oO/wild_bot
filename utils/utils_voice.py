import sqlite3


#добавление нового голосующего
def new_people_voice(id, username, money=0, count_attems = 0, status = 1):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS people_voice(
                   id INTEGER,
                   username TEXT,
                   money INTEGER,
                   count_attems INTEGER,
                   status INTEGER
                   )""")

    cursor.execute("INSERT INTO people_voice VALUES(?, ?, ?, ?, ?);", (id, username, money, count_attems, status))

    conn.commit()
    conn.close

#выход/вход в панель голосующего
def update_in_voice(id, status):
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE people_voice SET status = ? WHERE id = ?", (status,id))

    conn.commit()
    conn.close()

# проверка голосующего на наличие в базе данных
def check_people_voice():
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people_voice")
    user_id = list(cursor.fetchall())

    conn.close()

    return [int(i[0]) for i in user_id]

#данные голосующего
def list_str_people_voice(id):
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people_voice")
    user_id = list(cursor.fetchall())

    conn.close()

    for i in user_id:
        if i[0] == id:
            return list(i)

# смена количества денег
def update_money_voice(id, money):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people_voice SET money = ? WHERE id = ?", (money, id))

    conn.commit()
    conn.close()

# смена количества опросов
def update_attems_voice(id, count_poll):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE people_voice SET count_attems = ? WHERE id = ?", (count_poll, id))

    conn.commit()
    conn.close()

new_people_voice(1061436384, "@" + "U883oo01")
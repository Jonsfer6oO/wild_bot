import sqlite3

#добавление админов
def sql_admin(user_id:int, username:str, price:int, percent:int, work_service: str, time:int, status_admin:int):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
                   user_id INTEGER,
                   username TEXT,
                   price INTEGER,
                   percent INTEGER,
                   work_service TEXT,
                   time INTEGER,
                   status_admin INTEGER
                   )""")

    cursor.execute("INSERT INTO admin VALUES(?, ?, ?, ?, ?, ?, ?);", (user_id, username, price, percent, work_service, time,status_admin))
    conn.commit()
    conn.close()

# валидация админов
def list_admin_sql():

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admin')
    user_id = cursor.fetchall()

    conn.close()

    return [int(i[0]) for i in user_id]

# список строк таблицы
def list_str_sql(id:int):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admin')
    user_id = cursor.fetchall()

    conn.close()

    for i in user_id:
        if i[0] == int(id):
            return list(i)

def update_data(id:int,price:int=None, percent:int=None, work_service:str = None, time:int = None, status_admin:int = None):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    list_data = list_str_sql(id)

    lst = [price, percent, work_service,time, status_admin]

    for i in range(len(lst)):
        if lst[i] != None:
            list_data[i+2] = lst[i]

    cursor.execute("UPDATE admin SET price = ? WHERE user_id = ?", (list_data[2], id))
    cursor.execute("UPDATE admin SET percent = ? WHERE user_id = ?", (list_data[3], id))
    cursor.execute("UPDATE admin SET work_service = ? WHERE user_id = ?", (list_data[4], id))
    cursor.execute("UPDATE admin SET time = ? WHERE user_id = ?", (list_data[5], id))
    cursor.execute("UPDATE admin SET status_admin = ? WHERE user_id = ?", (list_data[6], id))

    conn.commit()
    conn.close()


# удаление админов
def del_admin_sql(id:int):

    conn = sqlite3.connect('admin.db')
    cursor=conn.cursor()

    cursor.execute("DELETE FROM admin WHERE user_id = ?", (id,))

    conn.commit()
    conn.close()

def update_status(id:int, work_service:str = None):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE admin SET work_service = ? WHERE user_id = ?", (work_service, id))


    conn.commit()
    conn.close()

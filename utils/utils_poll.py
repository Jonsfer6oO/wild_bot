import sqlite3

def sql_status(poll_id, poll_status, customer, id_customer):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS poll(
                   poll_id INTEGER,
                   poll_status INTEGER,
                   customer TEXT,
                   id_customer INTEGER
                   )""")

    cursor.execute("INSERT INTO poll VALUES(?, ?, ?, ?);",(poll_id,poll_status,customer,id_customer))


    conn.commit()
    conn.close()

def list_str_poll():

    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM poll")
    poll_id = cursor.fetchall()

    conn.close()

    return list(poll_id[-1])

def upgrate_poll(id, status_poll):

    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE poll SET poll_status = ? WHERE poll_id = ?", (status_poll, id))

    conn.commit()
    conn.close()

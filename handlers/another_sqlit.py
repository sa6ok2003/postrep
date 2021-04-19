import sqlite3

def check_channels(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT user FROM user_time WHERE id ={id}").fetchall()
    return a

def return_chatid_channel(username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT channel FROM user_time WHERE user = '{username}'").fetchone()
    return a[0]
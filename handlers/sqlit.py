import sqlite3
def reg_user(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id,
        channel,
        user
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id = {id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?,?)", (id, 0, 0 ))
        db.commit()


def update_user(id,channel,user):
    db = sqlite3.connect('server.db')
    sql = db.cursor()


    sql.execute(f"SELECT id FROM user_time WHERE id ={id} and channel = {channel}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?,?)", (id, channel,user))
        db.commit()

def red_goodchannel(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS goodchannel (
            id,
            data_finish
            ) """)
    db.commit()
    sql.execute(f"SELECT id FROM goodchannel WHERE id = '{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO goodchannel VALUES (?,?)", (f'{id}', 1))
        db.commit()

def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a

def info_channel():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT id FROM goodchannel').fetchall()

    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    id = name[1:]
    sql.execute(f"SELECT id FROM goodchannel WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO goodchannel VALUES (?,?)", (id, 1))
        db.commit()
    db.commit()

def del_one_channel(name): #Удаление одного канала
    print('Hello')
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    id = name[1:]
    print(id)
    sql.execute(f"SELECT id FROM goodchannel WHERE id ='{id}'")
    if sql.fetchone() is None:
        print('123')
    else:
        print(432)
        sql.execute(f'DELETE FROM goodchannel WHERE id ="{id}"')
        db.commit()

def proverka (id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM goodchannel WHERE id ='{id}'")
    if sql.fetchone() is None:
        return 0
    else: return 1
import sqlite3

db = sqlite3.connect('datebase.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""
    CREATE TABLE IF NOT EXISTS tb_users (
        user_id TEXT,
        user_quality TEXT
    )
""")
db.commit()


def check_user_id(user_id):
    query = f"SELECT user_id FROM tb_users WHERE user_id = '{user_id}'"
    sql.execute(query)
    result = sql.fetchone()
    return result


def insert_user_quality(user_id, user_quality):
    query = f"INSERT INTO tb_users VALUES ('{user_id}', '{user_quality}')"
    sql.execute(query)
    db.commit()


def update_user_quality(user_id, user_quality):
    query = f'UPDATE tb_users SET user_quality = "{user_quality}" WHERE user_id = "{user_id}"'
    sql.execute(query)
    db.commit()


def select_user_quality(user_id):
    query = f"SELECT user_quality FROM tb_users WHERE user_id = '{user_id}'"
    sql.execute(query)
    result = sql.fetchone()
    return result[0]


def get_user_quality(user_id):
    query = f"SELECT user_quality FROM tb_users WHERE user_id = '{user_id}'"
    sql.execute(query)
    result = sql.fetchone()
    return result[0]


def get_all():
    query = f"SELECT * FROM tb_users"
    sql.execute(query)
    result = sql.fetchall()
    return result

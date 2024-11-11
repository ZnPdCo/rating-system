import sqlite3 as sl
from database import connect_db
import string
import random


def check_login(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (id, ))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return False
    else:
        return True


def check_admin(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT admin FROM users WHERE id=?", (id, ))
    admin = cursor.fetchone()
    conn.close()
    if admin is None:
        return False
    elif admin[0] == 0:
        return False
    else:
        return True


def get_username(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id=?", (id, ))
    username = cursor.fetchone()
    conn.close()
    if username is None:
        return None
    else:
        return username[0]


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

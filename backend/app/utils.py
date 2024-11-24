"""
Filename: utils.py
Author: ZnPdCo
"""

import string
import random
import numpy as np
import app.constants
from app.database import connect_db


def check_login(uid):
    """
    Check if the user with the given id exists in the database.

    Returns:
        True if the user exists, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT permission FROM users WHERE id=%s", (uid,))
    permission = cursor.fetchone()
    conn.close()
    if permission is None:
        return False
    if permission[0] & app.constants.permission["login"]:
        return True
    return False


def check_vote(uid):
    """
    Check if the user with the given id can vote.

    Returns:
        True if the user can vote, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT permission FROM users WHERE id=%s", (uid,))
    permission = cursor.fetchone()
    conn.close()
    if permission is None:
        return False
    if permission[0] & app.constants.permission["vote"]:
        return True
    return False


def check_admin(uid):
    """
    Check if the user with the given id is an admin.

    Returns:
        True if the user is an admin, False otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT permission FROM users WHERE id=%s", (uid,))
    permission = cursor.fetchone()
    conn.close()
    if permission is None:
        return False
    if permission[0] & app.constants.permission["admin"]:
        return True
    return False


def get_username(uid):
    """
    Get the username of the user with the given id.

    Returns:
        The username of the user if it exists, None otherwise.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id=%s", (uid,))
    username = cursor.fetchone()
    conn.close()
    if username is None:
        return None
    return username[0]


def random_string(length):
    """
    Generate a random string of lowercase letters of the given length.

    Returns:
        The random string.
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def update_rating(pid):
    """
    Update the rating of the problem with the given id.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM difficulty WHERE pid=%s", (pid,))
    res = cursor.fetchall()
    difficulty = [item[0] for item in res]
    cursor.execute("SELECT val FROM quality WHERE pid=%s", (pid,))
    res = cursor.fetchall()
    quality = [item[0] for item in res]

    difficulty1 = sum(difficulty) / len(difficulty) if len(difficulty) > 0 else None
    quality1 = sum(quality) / len(quality) if len(quality) > 0 else None
    difficulty2 = np.median(np.array(difficulty)) if len(difficulty) > 0 else None
    quality2 = np.median(np.array(quality)) if len(quality) > 0 else None

    if difficulty1 is None:
        cursor.execute("UPDATE problems SET difficulty=null WHERE pid=%s", (pid,))
    else:
        cursor.execute(
            "UPDATE problems SET difficulty=%s WHERE pid=%s", (difficulty1, pid)
        )

    if difficulty2 is None:
        cursor.execute("UPDATE problems SET difficulty2=null WHERE pid=%s", (pid,))
    else:
        cursor.execute(
            "UPDATE problems SET difficulty2=%s WHERE pid=%s", (difficulty2, pid)
        )

    if quality1 is None:
        cursor.execute("UPDATE problems SET quality=null WHERE pid=%s", (pid,))
    else:
        cursor.execute("UPDATE problems SET quality=%s WHERE pid=%s", (quality1, pid))

    if quality2 is None:
        cursor.execute("UPDATE problems SET quality2=null WHERE pid=%s", (pid,))
    else:
        cursor.execute("UPDATE problems SET quality2=%s WHERE pid=%s", (quality2, pid))

    cursor.execute(
        "UPDATE problems SET cnt1=%s, cnt2=%s WHERE pid=%s",
        (len(difficulty), len(quality), pid),
    )
    conn.commit()
    conn.close()

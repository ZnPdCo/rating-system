"""
Filename: vote/api.py
Author: ZnPdCo
"""

from app.database import connect_db
from app.utils import random_string, update_rating


def vote(username, difficulty, quality, comment, pid):
    """
    Vote for a problem.
    """

    rating_id = random_string(128)

    if difficulty == -1 or 800 <= difficulty <= 3500:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM difficulty WHERE username=? AND pid=?",
            (username, pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM difficulty WHERE username=? AND pid=?",
                (username, pid),
            )
        if difficulty != -1:
            cursor.execute(
                "INSERT INTO difficulty (username, pid, val, id) VALUES (?,?,?,?)",
                (username, pid, difficulty, rating_id),
            )
        conn.commit()
        conn.close()

    if quality == -1 or 0 <= quality <= 5:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM quality WHERE username=? AND pid=?",
            (username, pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM quality WHERE username=? AND pid=?",
                (username, pid),
            )
        if quality != -1:
            cursor.execute(
                "INSERT INTO quality (username, pid, val, id) VALUES (?,?,?,?)",
                (username, pid, quality, rating_id),
            )
        conn.commit()
        conn.close()

    if len(comment) <= 500:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM comment WHERE username=? AND pid=?",
            (username, pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM comment WHERE username=? AND pid=?",
                (username, pid),
            )
        if comment != "":
            cursor.execute(
                "INSERT INTO comment (username, pid, val, id) VALUES (?,?,?,?)",
                (username, pid, comment, rating_id),
            )
        conn.commit()
        conn.close()

    update_rating(pid)


def get_vote(username, pid):
    """
    Get my vote for a problem.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT val FROM difficulty WHERE pid=? AND username=?",
        (pid, username),
    )
    difficulty = cursor.fetchone()
    cursor.execute(
        "SELECT val FROM quality WHERE pid=? AND username=?",
        (pid, username),
    )
    quality = cursor.fetchone()
    cursor.execute(
        "SELECT val FROM comment WHERE pid=? AND username=?",
        (pid, username),
    )
    comment = cursor.fetchone()
    conn.close()
    if difficulty is None:
        difficulty = -1
    else:
        difficulty = difficulty[0]
    if quality is None:
        quality = -1
    else:
        quality = quality[0]
    if comment is None:
        comment = ""
    else:
        comment = comment[0]
    res = {"difficulty": difficulty, "quality": quality, "comment": comment}
    return res


def get_votes(pid):
    """
    Get all votes for a problem.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, val, id FROM difficulty WHERE pid=?", (pid,))
    difficulty = cursor.fetchall()
    cursor.execute("SELECT username, val, id FROM quality WHERE pid=?", (pid,))
    quality = cursor.fetchall()
    cursor.execute("SELECT username, val, id FROM comment WHERE pid=?", (pid,))
    comment = cursor.fetchall()

    rating = {}
    for item in difficulty:
        if rating.get(item[0]) is None:
            rating[item[0]] = {
                "difficulty": None,
                "quality": None,
                "comment": None,
                "id": None,
            }
        rating[item[0]]["difficulty"] = item[1]
        rating[item[0]]["id"] = item[2]
    for item in quality:
        if rating.get(item[0]) is None:
            rating[item[0]] = {
                "difficulty": None,
                "quality": None,
                "comment": None,
                "id": None,
            }
        rating[item[0]]["quality"] = item[1]
        rating[item[0]]["id"] = item[2]
    for item in comment:
        if rating.get(item[0]) is None:
            rating[item[0]] = {
                "difficulty": None,
                "quality": None,
                "comment": None,
                "id": None,
            }
        rating[item[0]]["comment"] = item[1]
        rating[item[0]]["id"] = item[2]

    res = []
    for item in rating.values():
        res.append(
            {
                "difficulty": item["difficulty"],
                "quality": item["quality"],
                "comment": item["comment"],
                "id": item["id"],
            }
        )

    return res


def report(idx):
    """
    Report a rating.
    """
    username = None
    difficulty = None
    quality = None
    comment = None
    pid = None

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, val, pid FROM difficulty WHERE id=?",
        (idx,),
    )
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        difficulty = res[1]
        pid = res[2]
    cursor.execute("SELECT username, val, pid FROM quality WHERE id=?", (idx,))
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        quality = res[1]
        pid = res[2]
    cursor.execute("SELECT username, val, pid FROM comment WHERE id=?", (idx,))
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        comment = res[1]
        pid = res[2]
    conn.close()

    if username is None:
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO report (username, pid, difficulty, quality, comment, id) VALUES (?,?,?,?,?,?)",
        (username, pid, difficulty, quality, comment, idx),
    )
    conn.commit()
    conn.close()


def get_reports():
    """
    Get all reports
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pid, difficulty, quality, comment, username FROM report")
    reports = cursor.fetchall()
    conn.close()
    res = []
    for item in reports:
        res.append(
            {
                "id": item[0],
                "pid": item[1],
                "difficulty": item[2],
                "quality": item[3],
                "comment": item[4],
                "username": item[5],
            }
        )
    return res


def update_report(idx, delete):
    """
    Update a report
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pid FROM report WHERE id=?", (idx,))
    pid = cursor.fetchone()
    if delete:
        cursor.execute("DELETE FROM difficulty WHERE id=?", (idx,))
        cursor.execute("DELETE FROM quality WHERE id=?", (idx,))
        cursor.execute("DELETE FROM comment WHERE id=?", (idx,))
    cursor.execute("DELETE FROM report WHERE id=?", (idx,))
    conn.commit()
    conn.close()
    if pid is not None:
        pid = pid[0]
        update_rating(pid)

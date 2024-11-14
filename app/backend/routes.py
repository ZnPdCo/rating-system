"""
Filename: backend/routes.py
Author: ZnPdCo
"""

import json
from flask import request, Blueprint
from app.database import connect_db
from app.utils import check_login, get_username, random_string, update_rating
from app.custom.auto_status import auto_status
from app.config import config

backend_bp = Blueprint("backend", __name__)


@backend_bp.route("/get_problems/", methods=["GET"])
def get_problems():
    """
    Get all problems from the database.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pid, contest, name, difficulty, \
                quality, difficulty2, quality2, \
                cnt1, cnt2, info FROM problems"
    )
    problems = cursor.fetchall()
    conn.close()
    res = []
    for problem in problems:
        res.append(
            {
                "pid": problem[0],
                "contest": problem[1],
                "name": problem[2],
                "difficulty": problem[3],
                "quality": problem[4],
                "difficulty2": problem[5],
                "quality2": problem[6],
                "cnt1": problem[7],
                "cnt2": problem[8],
                "info": json.loads(problem[9]),
            }
        )
    return json.dumps(res), 200, {"Content-Type": "application/json"}


@backend_bp.route("/vote/", methods=["POST"])
def vote():
    """
    Vote for a problem.
    """
    if not check_login(request.cookies.get("id")):
        return ""
    if request.form.get("pid") is None:
        return ""

    difficulty = int(request.form.get("difficulty"))
    quality = int(request.form.get("quality"))
    comment = request.form.get("comment")
    pid = int(request.form.get("pid"))

    rating_id = random_string(128)

    if difficulty == -1 or 800 <= difficulty <= 3500:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM difficulty WHERE username=? AND pid=?",
            (get_username(request.cookies.get("id")), pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM difficulty WHERE username=? AND pid=?",
                (get_username(request.cookies.get("id")), pid),
            )
        if difficulty != -1:
            cursor.execute(
                "INSERT INTO difficulty (username, pid, val, id) VALUES (?,?,?,?)",
                (get_username(request.cookies.get("id")), pid, difficulty, rating_id),
            )
        conn.commit()
        conn.close()

    if quality == -1 or 1 <= quality <= 5:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM quality WHERE username=? AND pid=?",
            (get_username(request.cookies.get("id")), pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM quality WHERE username=? AND pid=?",
                (get_username(request.cookies.get("id")), pid),
            )
        if quality != -1:
            cursor.execute(
                "INSERT INTO quality (username, pid, val, id) VALUES (?,?,?,?)",
                (get_username(request.cookies.get("id")), pid, quality, rating_id),
            )
        conn.commit()
        conn.close()

    if len(comment) <= 500:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute(
            "SELECT * FROM comment WHERE username=? AND pid=?",
            (get_username(request.cookies.get("id")), pid),
        )
        if res.fetchone() is not None:
            cursor.execute(
                "DELETE FROM comment WHERE username=? AND pid=?",
                (get_username(request.cookies.get("id")), pid),
            )
        if comment != "":
            cursor.execute(
                "INSERT INTO comment (username, pid, val, id) VALUES (?,?,?,?)",
                (get_username(request.cookies.get("id")), pid, comment, rating_id),
            )
        conn.commit()
        conn.close()

    update_rating(pid)

    return ""


@backend_bp.route("/get_vote/", methods=["POST"])
def get_vote():
    """
    Get my vote for a problem.
    """
    if not check_login(request.cookies.get("id")):
        return ""
    if request.form.get("pid") is None:
        return ""
    pid = int(request.form.get("pid"))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT val FROM difficulty WHERE pid=? AND username=?",
        (pid, get_username(request.cookies.get("id"))),
    )
    difficulty = cursor.fetchone()
    cursor.execute(
        "SELECT val FROM quality WHERE pid=? AND username=?",
        (pid, get_username(request.cookies.get("id"))),
    )
    quality = cursor.fetchone()
    cursor.execute(
        "SELECT val FROM comment WHERE pid=? AND username=?",
        (pid, get_username(request.cookies.get("id"))),
    )
    comment = cursor.fetchone()
    conn.close()
    if difficulty is None:
        difficulty = 0
    else:
        difficulty = difficulty[0]
    if quality is None:
        quality = 0
    else:
        quality = quality[0]
    if comment is None:
        comment = ""
    else:
        comment = comment[0]
    res = {"difficulty": difficulty, "quality": quality, "comment": comment}
    return json.dumps(res), 200, {"Content-Type": "application/json"}


@backend_bp.route("/get_votes/", methods=["POST"])
def get_votes():
    """
    Get all votes for a problem.
    """
    if request.form.get("pid") is None:
        return ""
    pid = int(request.form.get("pid"))
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

    return json.dumps(res), 200, {"Content-Type": "application/json"}


@backend_bp.route("/report/", methods=["POST"])
def report():
    """
    Report a rating.
    """
    if not check_login(request.cookies.get("id")):
        return ""
    if request.form.get("id") is None:
        return ""
    username = None
    difficulty = None
    quality = None
    comment = None
    pid = None

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, val, pid FROM difficulty WHERE id=?",
        (request.form.get("id"),),
    )
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        difficulty = res[1]
        pid = res[2]
    cursor.execute(
        "SELECT username, val, pid FROM quality WHERE id=?", (request.form.get("id"),)
    )
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        quality = res[1]
        pid = res[2]
    cursor.execute(
        "SELECT username, val, pid FROM comment WHERE id=?", (request.form.get("id"),)
    )
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        comment = res[1]
        pid = res[2]
    conn.close()

    if username is None:
        return ""

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO report (username, pid, difficulty, quality, comment, id) VALUES (?,?,?,?,?,?)",
        (username, pid, difficulty, quality, comment, request.form.get("id")),
    )
    conn.commit()
    conn.close()

    return ""


def auto_update_status(username):
    """
    Auto update the status of user. (convert from OJ pid to System pid)
    """
    oj_status = auto_status(username)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE username=?", (username,))
    system_status = json.loads(cursor.fetchone()[0])
    for oj_pid, status in oj_status.items():
        cursor.execute("SELECT pid FROM problems WHERE ojpid=?", (oj_pid,))
        system_pid = cursor.fetchone()
        if system_pid is None:
            continue
        system_pid = str(system_pid[0])
        if system_pid in system_status:
            system_status[system_pid] = max(system_status[system_pid], status)
        else:
            system_status[system_pid] = status
    cursor.execute(
        "UPDATE users SET status=? WHERE username=?",
        (json.dumps(system_status), username),
    )
    conn.commit()
    conn.close()


@backend_bp.route("/get_status/", methods=["POST"])
def get_status():
    """
    Get the status of a user.
    """
    if not check_login(request.cookies.get("id")):
        return "{}", 200, {"Content-Type": "application/json"}

    username = get_username(request.cookies.get("id"))

    if config["auto_status"]:
        auto_update_status(username)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE username=?", (username,))
    res = cursor.fetchone()
    if res is None:
        return ""
    status = res[0]
    conn.close()
    return status, 200, {"Content-Type": "application/json"}


@backend_bp.route("/update_status/", methods=["POST"])
def update_status():
    """
    Update the status of a user.
    """
    if config["auto_status"]:
        return ""
    if not check_login(request.cookies.get("id")):
        return ""
    if request.values.get("status") is None:
        return ""
    username = get_username(request.cookies.get("id"))
    status = request.values.get("status")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status=? WHERE username=?", (status, username))
    conn.commit()
    conn.close()
    return ""

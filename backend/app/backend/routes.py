"""
Filename: backend/routes.py
Author: ZnPdCo
"""

import json
from flask import request, Blueprint
from app.database import connect_db
from app.utils import check_login, get_username
from app.custom.auto_status import auto_status
from app.config import config
from app.announcement.api import get_announcement
from app.problem.api import get_problems
from app.vote.api import vote, get_vote, get_votes, report

backend_bp = Blueprint("backend", __name__)


@backend_bp.route("/get_problems/", methods=["GET"])
def get_problems_route():
    """
    Get all problems from the database.
    """
    return json.dumps(get_problems()), 200, {"Content-Type": "application/json"}


@backend_bp.route("/vote/", methods=["POST"])
def vote_route():
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

    vote(get_username(request.cookies.get("id")), difficulty, quality, comment, pid)

    return ""


@backend_bp.route("/get_vote/", methods=["POST"])
def get_vote_route():
    """
    Get my vote for a problem.
    """
    if not check_login(request.cookies.get("id")):
        return ""
    if request.form.get("pid") is None:
        return ""
    pid = int(request.form.get("pid"))
    username = get_username(request.cookies.get("id"))
    return (
        json.dumps(get_vote(username, pid)),
        200,
        {"Content-Type": "application/json"},
    )


@backend_bp.route("/get_votes/", methods=["POST"])
def get_votes_route():
    """
    Get all votes for a problem.
    """
    if request.form.get("pid") is None:
        return ""
    pid = int(request.form.get("pid"))

    return json.dumps(get_votes(pid)), 200, {"Content-Type": "application/json"}


@backend_bp.route("/report/", methods=["POST"])
def report_route():
    """
    Report a rating.
    """
    if not check_login(request.cookies.get("id")):
        return ""
    if request.form.get("id") is None:
        return ""

    report(request.form.get("id"))

    return ""


def auto_update_status(username):
    """
    Auto update the status of user. (convert from OJ pid to System pid)
    """
    oj_status = auto_status(username)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM users WHERE username=%s", (username,))
    system_status = json.loads(cursor.fetchone()[0])
    for oj_pid, status in oj_status.items():
        cursor.execute("SELECT pid FROM problems WHERE ojpid=%s", (oj_pid,))
        system_pid = cursor.fetchone()
        if system_pid is None:
            continue
        system_pid = str(system_pid[0])
        if system_pid in system_status:
            system_status[system_pid] = max(system_status[system_pid], status)
        else:
            system_status[system_pid] = status
    cursor.execute(
        "UPDATE users SET status=%s WHERE username=%s",
        (json.dumps(system_status), username),
    )
    conn.commit()
    conn.close()


@backend_bp.route("/get_status/", methods=["POST"])
def get_status_route():
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
    cursor.execute("SELECT status FROM users WHERE username=%s", (username,))
    res = cursor.fetchone()
    if res is None:
        return ""
    status = res[0]
    conn.close()
    return status, 200, {"Content-Type": "application/json"}


@backend_bp.route("/update_status/", methods=["POST"])
def update_status_route():
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
    cursor.execute("UPDATE users SET status=%s WHERE username=%s", (status, username))
    conn.commit()
    conn.close()
    return ""


@backend_bp.route("/get_announcement/", methods=["POST"])
def get_announcement_route():
    """
    Get the latest announcement.
    """
    return get_announcement()

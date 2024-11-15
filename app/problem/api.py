"""
Filename: problem/api.py
Author: ZnPdCo
"""

import json
from app.database import connect_db


def add_problem(contest, name, info):
    """
    Add a problem
    """
    conn = connect_db()
    cursor = conn.cursor()
    # have same pid
    if "pid" in info:
        cursor.execute("SELECT contest FROM problems WHERE OJpid =?", (info["pid"],))
        res = cursor.fetchone()
        if res is not None:
            cursor.execute(
                "UPDATE problems SET contest = ? WHERE OJpid = ?",
                (contest + "(" + name + ")" + "," + res[0], info["pid"]),
            )
            conn.commit()
            conn.close()
            return
    cursor.execute(
        "INSERT INTO problems (OJpid, contest, name, info) VALUES (?,?,?,?)",
        (
            (info["pid"] if "pid" in info else ""),
            contest,
            name,
            json.dumps(info),
        ),
    )
    conn.commit()
    conn.close()


def update_problem(pid, contest, name, info):
    """
    Update a problem
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE problems SET OJpid=?, contest=?, name=?, info=? WHERE pid=?",
        (
            (info["pid"] if "pid" in info else ""),
            contest,
            name,
            json.dumps(info),
            pid,
        ),
    )
    conn.commit()
    conn.close()


def delete_problem(pid):
    """
    Delete a problem
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM problems WHERE pid=?", (pid,))
    conn.commit()
    conn.close()

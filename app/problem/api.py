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
    return res

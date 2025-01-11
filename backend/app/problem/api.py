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
        cursor.execute(
            "SELECT contest, info FROM problems WHERE oj_pid =%s", (info["pid"],)
        )
        res = cursor.fetchone()
        if res is not None:
            # 如果两个都拥有type，则将它们合并
            if "type" in info and "type" in json.loads(res[1]):
                info["type"] = list(set(json.loads(res[1])["type"] + info["type"]))
            cursor.execute(
                "UPDATE problems SET contest = %s, info = %s WHERE oj_pid = %s",
                (
                    contest + "(" + name + ")" + "," + res[0],
                    json.dumps(info),
                    info["pid"],
                ),
            )
            conn.commit()
            conn.close()
            return
    cursor.execute(
        "INSERT INTO problems (oj_pid, contest, name, info) VALUES (%s,%s,%s,%s)",
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
        "UPDATE problems SET oj_pid=%s, contest=%s, name=%s, info=%s WHERE pid=%s",
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
    cursor.execute("DELETE FROM problems WHERE pid=%s", (pid,))
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
                difficulty_cnt, quality_cnt, info FROM problems"
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
                "difficulty_cnt": problem[7],
                "quality_cnt": problem[8],
                "info": json.loads(problem[9]),
            }
        )
    return res

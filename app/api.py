"""
Filename: admin/base.py
Author: ZnPdCo
"""

import json
from app.database import connect_db


def add_problem(contest, name, info):
    """
    Add a problem with params
    """
    conn = connect_db()
    cursor = conn.cursor()
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

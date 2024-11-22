"""
Filename: announcement/api.py
Author: ZnPdCo
"""

from app.database import connect_db


def update_announcement(announcement):
    """
    Update announcement with params
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM announcement")
    cursor.execute(
        "INSERT INTO announcement (announcement) VALUES (%s)",
        (announcement,),
    )
    conn.commit()
    conn.close()


def get_announcement():
    """
    Get the latest announcement
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT announcement FROM announcement")
    res = cursor.fetchone()
    conn.close()
    return res[0] if res is not None else ""

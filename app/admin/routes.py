"""
Filename: admin/routes.py
Author: ZnPdCo
"""

import json
from flask import render_template, request, Blueprint, redirect
from app.database import connect_db
from app.utils import check_admin, update_rating

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/", methods=["GET"])
def admin():
    """
    Admin page
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    return render_template(
        "admin.html",
    )


@admin_bp.route("/edit_permissions/", methods=["POST"])
def edit_permissions():
    """
    Edit user permissions
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET admin=? WHERE username=?",
        (request.form.get("admin"), request.form.get("username")),
    )
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/add_problem/", methods=["POST"])
def add_problem():
    """
    Add a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (OJpid, contest, name, info) VALUES (?,?,?,?)",
        (
            json.loads(request.form.get("info"))["pid"] if "pid" in json.loads(request.form.get("info")) else "",
            request.form.get("contest"),
            request.form.get("name"),
            request.form.get("info"),
        ),
    )
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/update_problem/", methods=["POST"])
def update_problem():
    """
    Update a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE problems SET OJpid=?, contest=?, name=?, info=? WHERE pid=?",
        (
            json.loads(request.form.get("info"))["pid"] if "pid" in json.loads(request.form.get("info")) else "",
            request.form.get("contest"),
            request.form.get("name"),
            request.form.get("info"),
            request.form.get("pid"),
        ),
    )
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/delete_problem/", methods=["POST"])
def delete_problem():
    """
    Delete a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM problems WHERE pid=?", (request.form.get("pid"),))
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/get_reports/", methods=["POST"])
def get_reports():
    """
    Get all reports
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pid, difficulty, quality, comment, username FROM report")
    reports = cursor.fetchall()
    conn.close()
    res = []
    for report in reports:
        res.append(
            {
                "id": report[0],
                "pid": report[1],
                "difficulty": report[2],
                "quality": report[3],
                "comment": report[4],
                "username": report[5],
            }
        )
    return json.dumps(res), 200, {"Content-Type": "application/json"}


@admin_bp.route("/update_report/", methods=["POST"])
def update_report():
    """
    Update a report
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pid FROM report WHERE id=?", (request.form.get("id"),))
    pid = cursor.fetchone()
    if request.form.get("delete") == "1":
        cursor.execute("DELETE FROM difficulty WHERE id=?", (request.form.get("id"),))
        cursor.execute("DELETE FROM quality WHERE id=?", (request.form.get("id"),))
        cursor.execute("DELETE FROM comment WHERE id=?", (request.form.get("id"),))
    cursor.execute("DELETE FROM report WHERE id=?", (request.form.get("id"),))
    conn.commit()
    conn.close()
    if pid is not None:
        pid = pid[0]
        update_rating(pid)
    return ""

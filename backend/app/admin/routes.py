"""
Filename: admin/routes.py
Author: ZnPdCo
"""

import json
import hashlib
import os
from flask import render_template, request, Blueprint, redirect, send_file
from app.database import connect_db
from app.utils import check_admin
from app.custom.auto_problems import auto_problems
from app.problem.api import add_problem, update_problem, delete_problem
from app.announcement.api import update_announcement
from app.vote.api import update_report, get_reports
from app.config import config

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/", methods=["GET"])
def admin_route():
    """
    Admin page
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    return render_template(
        "index.html",
    )


@admin_bp.route("/edit_permissions/", methods=["POST"])
def edit_permissions_route():
    """
    Edit user permissions
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE admin=1")
    admins = cursor.fetchall()
    if (
        len(admins) == 1
        and request.form.get("username") == admins[0][0]
        and request.form.get("admin") == "0"
    ):
        conn.close()
        return "Cannot remove the only admin"
    cursor.execute(
        "UPDATE users SET admin=%s WHERE username=%s",
        (request.form.get("admin"), request.form.get("username")),
    )
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/get_users/", methods=["POST"])
def get_users_route():
    """
    Get all users
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, admin FROM users")
    users = cursor.fetchall()
    conn.close()
    res = []
    for user in users:
        res.append({"username": user[0], "admin": user[1]})
    return json.dumps(res), 200, {"Content-Type": "application/json"}


@admin_bp.route("/update_user_password/", methods=["POST"])
def update_user_password_route():
    """
    update user password
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password=%s WHERE username=%s",
        (
            hashlib.sha256(request.form.get("password").encode("utf-8")).hexdigest(),
            request.form.get("username"),
        ),
    )
    conn.commit()
    conn.close()
    return redirect("/admin/")


@admin_bp.route("/add_problem/", methods=["POST"])
def add_problem_route():
    """
    Add a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    add_problem(
        request.form.get("contest"),
        request.form.get("name"),
        json.loads(request.form.get("info")),
    )
    return redirect("/admin/")


@admin_bp.route("/update_problem/", methods=["POST"])
def update_problem_route():
    """
    Update a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    update_problem(
        request.form.get("pid"),
        request.form.get("contest"),
        request.form.get("name"),
        json.loads(request.form.get("info")),
    )
    return redirect("/admin/")


@admin_bp.route("/delete_problem/", methods=["POST"])
def delete_problem_route():
    """
    Delete a problem
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    delete_problem(request.form.get("pid"))
    return redirect("/admin/")


@admin_bp.route("/get_reports/", methods=["POST"])
def get_reports_route():
    """
    Get all reports
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    return json.dumps(get_reports()), 200, {"Content-Type": "application/json"}


@admin_bp.route("/update_report/", methods=["POST"])
def update_report_route():
    """
    Update a report
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    update_report(request.form.get("id"), request.form.get("delete") == "1")
    return ""


@admin_bp.route("/auto_update_problems/", methods=["POST"])
def auto_update_problems_route():
    """
    Auto update problems
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    auto_problems(json.loads(request.form.get("params")))
    return redirect("/admin/")


@admin_bp.route("/update_announcement/", methods=["POST"])
def update_announcement_route():
    """
    Update announcement
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    update_announcement(request.form.get("announcement"))
    return redirect("/admin/")

@admin_bp.route("/export_database/", methods=["GET"])
def export_database_route():
    """
    Export database
    """
    if not check_admin(request.cookies.get("id")):
        return redirect("/")
    sqlfromat = "mysqldump -h%s -u%s -p%s -P%s %s > database.sql"
    sql = (sqlfromat % (config['db_host'],
                        config['db_user'],
                        config['db_password'],
                        config['db_port'],
                        config['db_name']))
    os.system(sql)
    return send_file("database.sql", as_attachment=True)

from flask import Flask, render_template, request, make_response, Blueprint, current_app
import sqlite3 as sl
import hashlib
import random
import string
import json
import numpy as np
from database import connect_db
from utils import check_login, check_admin, get_username, random_string

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=['GET'])
def admin():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    return render_template('admin.html',
                           title=current_app.config['TITLE'],
                           logged_in=check_login(request.cookies.get('id')),
                           is_admin=check_admin(request.cookies.get('id')))


@admin_bp.route('/edit_permissions/', methods=['POST'])
def edit_permissions():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET admin=? WHERE username=?",
                   (request.form.get("admin"), request.form.get("username")))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"


@admin_bp.route('/add_problem/', methods=['POST'])
def add_problem():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO problems (contest, name, info) VALUES (?,?,?)",
                   (request.form.get("contest"), request.form.get("name"),
                    request.form.get("info")))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"


@admin_bp.route('/update_problem/', methods=['POST'])
def update_problem():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE problems SET contest=?, name=?, info=? WHERE pid=?",
                   (request.form.get("contest"), request.form.get("name"),
                    request.form.get("info"), request.form.get("pid")))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"


@admin_bp.route('/delete_problem/', methods=['POST'])
def delete_problem():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM problems WHERE pid=?",
                   (request.form.get("pid"), ))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"


@admin_bp.route('/get_reports/', methods=['POST'])
def get_reports():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, pid, difficulty, quality, comment, username FROM report")
    reports = cursor.fetchall()
    conn.close()
    res = []
    for report in reports:
        res.append({
            "id": report[0],
            "pid": report[1],
            "difficulty": report[2],
            "quality": report[3],
            "comment": report[4],
            "username": report[5]
        })
    return json.dumps(res), 200, {"Content-Type": "application/json"}


@admin_bp.route('/update_report/', methods=['POST'])
def update_report():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pid FROM report WHERE id=?",
                   (request.form.get("id"), ))
    pid = cursor.fetchone()
    if request.form.get("delete") == "1":
        cursor.execute("DELETE FROM difficulty WHERE id=?",
                       (request.form.get("id"), ))
        cursor.execute("DELETE FROM quality WHERE id=?",
                       (request.form.get("id"), ))
        cursor.execute("DELETE FROM comment WHERE id=?",
                       (request.form.get("id"), ))
    cursor.execute("DELETE FROM report WHERE id=?", (request.form.get("id"), ))
    conn.commit()
    conn.close()
    if pid is not None:
        pid = pid[0]
        update_rating(pid)
    return ""

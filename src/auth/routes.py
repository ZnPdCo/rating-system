"""
Filename: auth/routes.py
Author: ZnPdCo
"""

import hashlib
from flask import render_template, request, make_response, Blueprint
from auth.verify import verify_account
from database import connect_db
from utils import random_string

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    """
    Login page
    """
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None and password is None:
        return render_template(
            "login.html",
        )
    if (
        len(username) == 0
        or len(username) > 100
        or len(password) == 0
        or len(password) > 100
    ):
        return "<script>location.search='?error=3';</script>"

    # check user exist
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        # register user
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM verify WHERE username=?", (username,))
        cursor.execute("DELETE FROM verify WHERE julianday('now') - julianday(created_at) >= 1")
        idx = random_string(128)
        cursor.execute("INSERT INTO verify (id, username, password, code) VALUES (?,?,?,?)", (idx, username, hashlib.sha256(password.encode("utf-8")).hexdigest(), random_string(10)))
        conn.commit()
        conn.close()
        return "<script>location.href='/verify?id=" + idx + "';</script>"

    # check password
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if hashlib.sha256(password.encode("utf-8")).hexdigest() != user[1]:
        return "<script>location.search='?error=1';</script>"
    conn.close()

    # if the first username, it is admin
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    res = cursor.fetchall()
    if len(res) == 1:
        cursor.execute("UPDATE users SET admin=1 WHERE id=?", (user[0],))
        conn.commit()
    conn.close()

    resp = make_response("<script>location.href='/';</script>")
    resp.set_cookie("id", user[0], httponly=False, max_age=3600 * 24 * 30)
    return resp


@auth_bp.route("/logout/", methods=["GET"])
def logout():
    """
    Logout page
    """
    resp = make_response("<script>location.href='/';</script>")
    resp.set_cookie("id", "", expires=0)
    return resp

@auth_bp.route("/verify/", methods=["GET", "POST"])
def verify():
    """
    Verify page
    """
    idx = request.args.get("id")
    if idx is None:
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM verify WHERE julianday('now') - julianday(created_at) >= 1")
    cursor.execute("SELECT username, password, code FROM verify WHERE id=?", (idx,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return "<script>location.href='/';</script>"
    username = user[0]
    password = user[1]
    code = user[2]
    if request.method == 'GET':
        return render_template(
            "verify.html",
            code=code,
        )
    if not verify_account(username, code):
        return "<script>location.search='?error=1&id=" + idx + "';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM verify WHERE id=?", (idx,))
    cursor.execute(
        "INSERT INTO users (id, username, password) VALUES (?,?,?)",
        (
            random_string(128),
            username,
            password,
        ),
    )
    conn.commit()
    conn.close()
    return "<script>location.href='/login/';</script>"

"""
Filename: auth/routes.py
Author: ZnPdCo
"""

import hashlib
from urllib import parse
from flask import render_template, request, Blueprint, redirect
from app.custom.verify import verify_account
from app.database import connect_db
from app.utils import random_string

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
        message = "username len in [1, 100], password len in [1, 100]"
        return redirect(f"/login/?error={parse.quote(message)}")

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
        cursor.execute(
            "DELETE FROM verify WHERE julianday('now') - julianday(created_at) >= 1"
        )
        idx = random_string(128)
        cursor.execute(
            "INSERT INTO verify (id, username, password, code) VALUES (?,?,?,?)",
            (
                idx,
                username,
                hashlib.sha256(password.encode("utf-8")).hexdigest(),
                random_string(10),
            ),
        )
        conn.commit()
        conn.close()
        return redirect(f"/verify?id={idx}")

    # check password
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if hashlib.sha256(password.encode("utf-8")).hexdigest() != user[1]:
        message = "Password or username is incorrect. Please try again."
        return redirect(f"/login/?error={parse.quote(message)}")
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

    resp = redirect("/")
    resp.set_cookie("id", user[0], httponly=False, max_age=3600 * 24 * 30)
    return resp


@auth_bp.route("/logout/", methods=["GET"])
def logout():
    """
    Logout page
    """
    resp = redirect("/")
    resp.set_cookie("id", "", expires=0)
    return resp


@auth_bp.route("/verify/", methods=["GET", "POST"])
def verify():
    """
    Verify page
    """
    idx = request.args.get("id")
    if idx is None:
        return redirect("/login/")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM verify WHERE julianday('now') - julianday(created_at) >= 1"
    )
    cursor.execute("SELECT username, password, code FROM verify WHERE id=?", (idx,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        message = "The verification code is expired or invalid, please try again."
        return redirect(f"/login/?error={parse.quote(message)}")
    username = user[0]
    password = user[1]
    code = user[2]
    if request.method == "GET":
        return render_template(
            "verify.html",
            code=code,
        )
    if not verify_account(username, code):
        message = "Your description is not start with the code, please try again."
        return redirect(f"/verify?id={idx}&error={parse.quote(message)}")
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
    message = "Your account has been created successfully, please login."
    return redirect(f"/login/?success={parse.quote(message)}")


@auth_bp.route("/update_password/", methods=["GET", "POST"])
def update_password():
    """
    Update password page
    """
    if request.method == "GET":
        return render_template(
            "update_password.html",
        )
    idx = request.cookies.get("id")
    if idx is None:
        return redirect("/login/")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if (
        len(old_password) == 0
        or len(old_password) > 100
        or len(new_password) == 0
        or len(new_password) > 100
    ):
        message = "old_password len in [1, 100], new_password len in [1, 100]"
        return redirect(f"/update_password/?error={parse.quote(message)}")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE id=?", (idx,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return redirect("/login/")
    if hashlib.sha256(old_password.encode("utf-8")).hexdigest() != user[0]:
        message = "Old password is incorrect. Please try again."
        return redirect(f"/update_password/?error={parse.quote(message)}")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET id=?, password=? WHERE id=?",
        (
            random_string(128),
            hashlib.sha256(new_password.encode("utf-8")).hexdigest(),
            idx,
        ),
    )
    conn.commit()
    conn.close()
    message = "Your password has been updated successfully, please login."
    return redirect(f"/login/?success={parse.quote(message)}")

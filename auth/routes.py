from flask import Flask, render_template, request, make_response, Blueprint, current_app
import sqlite3 as sl
import hashlib
import random
import string
import json
import numpy as np
from database import connect_db
from utils import check_login, check_admin, get_username, random_string

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None and password is None:
        return render_template('login.html',
                               title=current_app.config['TITLE'],
                               logged_in=check_login(
                                   request.cookies.get('id')),
                               is_admin=check_admin(request.cookies.get('id')))
    else:
        if len(username) == 0 or len(username) > 100 or len(
                password) == 0 or len(password) > 100:
            return "<script>location.search='?error=3';</script>"

        # check user exist
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username, ))
        user = cursor.fetchone()
        if user is None:
            if False:
                return "<script>location.search='?error=2';</script>"
            # register user
            cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?,?,?)",
                (random_string(128), username,
                 hashlib.sha256(password.encode('utf-8')).hexdigest()))
            conn.commit()
        conn.close()

        # check password
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=?",
                       (username, ))
        user = cursor.fetchone()
        if hashlib.sha256(password.encode('utf-8')).hexdigest() != user[1]:
            return "<script>location.search='?error=1';</script>"
        conn.close()

        # if the first username, it is admin
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        res = cursor.fetchall()
        if len(res) == 1:
            cursor.execute("UPDATE users SET admin=1 WHERE id=?", (user[0], ))
            conn.commit()
        conn.close()

        resp = make_response("<script>location.href='/';</script>")
        resp.set_cookie('id', user[0], httponly=False, max_age=3600 * 24 * 30)
        return resp


@auth_bp.route('/logout/', methods=['GET'])
def logout():
    resp = make_response("<script>location.href='/';</script>")
    resp.set_cookie('id', '', expires=0)
    return resp

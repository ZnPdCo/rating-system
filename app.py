from flask import Flask, render_template, request, make_response
import sqlite3 as sl
import hashlib
import random
import string
import json

app = Flask(__name__)
title = 'Rating System'

def connect_db():
    try:
        conn = sl.connect('rating.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS problems (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
    contest VARCHAR(2048), 
    name VARCHAR(2048), 
    rating DOUBLE DEFAULT null,
    quality DOUBLE DEFAULT null,
    rating2 DOUBLE DEFAULT null,
    quality2 DOUBLE DEFAULT null,
    cnt1 INTEGER DEFAULT 0,
    cnt2 INTEGER DEFAULT 0,
    info json
); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(2048) PRIMARY KEY,
    username VARCHAR(2048),
    password VARCHAR(2048),
    admin INTEGER DEFAULT 0
); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS rating (
	username VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS quality (
	username VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS comment (
	username VARCHAR(2048), 
    pid INTEGER, 
    val VARCHAR(2048)
    ); 
                    """)
        conn.commit()
    except sl.Error as e:
        conn = None
    return conn

def check_login(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (id, ))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return False
    else:
        return True

def check_admin(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT admin FROM users WHERE id=?", (id, ))
    admin = cursor.fetchone()
    conn.close()
    if admin is None:
        return False
    elif admin[0] == 0:
        return False
    else:
        return True


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=title, logged_in=check_login(request.cookies.get('id')), is_admin=check_admin(request.cookies.get('id')))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None and password is None:
        return render_template('login.html', title=title, logged_in=check_login(request.cookies.get('id')), is_admin=check_admin(request.cookies.get('id')))
    else:
        # check user exist
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username, ))
        user = cursor.fetchone()
        if user is None:
            if False:
                return "<script>location.search='?error=2';</script>"
            # register user
            cursor.execute("INSERT INTO users (id, username, password) VALUES (?,?,?)", (random_string(128), username, hashlib.sha256(password.encode('utf-8')).hexdigest()))
            conn.commit()
        conn.close()

        # check password
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=?", (username, ))
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
        resp.set_cookie('id', user[0], httponly=False, max_age=3600*24*30)
        return resp

@app.route('/legal/', methods=['GET'])
def legal():
    return render_template('legal.html', title=title, logged_in=check_login(request.cookies.get('id')), is_admin=check_admin(request.cookies.get('id')))

@app.route('/admin/', methods=['GET'])
def admin():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    return render_template('admin.html', title=title, logged_in=check_login(request.cookies.get('id')), is_admin=check_admin(request.cookies.get('id')))

@app.route('/admin/edit_permissions/', methods=['POST'])
def edit_permissions():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET admin=? WHERE username=?", (request.form.get("admin"), request.form.get("username")))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"

@app.route('/admin/add_problem/', methods=['POST'])
def add_problem():
    if not check_admin(request.cookies.get('id')):
        return "<script>location.href='/';</script>"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO problems (contest, name, info) VALUES (?,?,?)", (request.form.get("contest"), request.form.get("name"), request.form.get("info")))
    conn.commit()
    conn.close()
    return "<script>location.href='/admin/';</script>"

@app.route('/backend/get_problems/', methods=['GET'])
def get_problems():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, contest, name, rating, quality, rating2, quality2, cnt1, cnt2, info FROM problems")
    problems = cursor.fetchall()
    conn.close()
    res = []
    for problem in problems:
        res.append({
            "id": problem[0],
            "contest": problem[1],
            "name": problem[2],
            "rating": problem[3],
            "quality": problem[4],
            "rating2": problem[5],
            "quality2": problem[6],
            "cnt1": problem[7],
            "cnt2": problem[8],
            "info": json.loads(problem[9])
        })
    return json.dumps(res), 200, {"Content-Type": "application/json"}

@app.route('/logout/', methods=['GET'])
def logout():
    resp = make_response("<script>location.href='/';</script>")
    resp.set_cookie('id', '', expires=0)
    return resp
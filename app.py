from flask import Flask, render_template, request, make_response
import sqlite3 as sl
import hashlib
import random
import string

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
    url VARCHAR(2048), 
    rating DOUBLE DEFAULT null,
    quality DOUBLE DEFAULT null,
    rating2 DOUBLE DEFAULT null,
    quality2 DOUBLE DEFAULT null,
    cnt1 INTEGER DEFAULT 0,
    cnt2 INTEGER DEFAULT 0
); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(2048) PRIMARY KEY,
    username VARCHAR(2048),
    password VARCHAR(2048)
); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS rating (
	id VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """)
        cursor.execute(""" 
CREATE TABLE IF NOT EXISTS quality (
	id VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """)
        conn.commit()
    except sl.Error as e:
        conn = None
    return conn

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=title)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None and password is None:
        return render_template('login.html', title=title)
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
            cursor.execute("INSERT INTO users (id, username, password) VALUES (?,?,?)", (''.join(random.choice(string.ascii_letters) for _ in range(128)), username, hashlib.sha256(password.encode('utf-8')).hexdigest()))
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

        resp = make_response("<script>location.href='/';</script>")
        resp.set_cookie('id', user[0], httponly=False, max_age=3600*24*30)
        return resp

@app.route('/legal/', methods=['GET'])
def legal():
    return render_template('legal.html', title=title)

@app.route('/logout/', methods=['GET'])
def logout():
    resp = make_response("<script>location.href='/';</script>")
    resp.set_cookie('id', '', expires=0)
    return resp
from flask import Flask, render_template, request, make_response, Blueprint, current_app
import sqlite3 as sl
import hashlib
import random
import string
import json
import numpy as np
from database import connect_db
from utils import check_login, check_admin, get_username, random_string

backend_bp = Blueprint('backend', __name__)

@backend_bp.route('/get_problems/', methods=['GET'])
def get_problems():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pid, contest, name, difficulty, quality, difficulty2, quality2, cnt1, cnt2, info FROM problems")
    problems = cursor.fetchall()
    conn.close()
    res = []
    for problem in problems:
        res.append({
            "pid": problem[0],
            "contest": problem[1],
            "name": problem[2],
            "difficulty": problem[3],
            "quality": problem[4],
            "difficulty2": problem[5],
            "quality2": problem[6],
            "cnt1": problem[7],
            "cnt2": problem[8],
            "info": json.loads(problem[9])
        })
    return json.dumps(res), 200, {"Content-Type": "application/json"}

def update_rating(pid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM difficulty WHERE pid=?", (pid, ))
    res = cursor.fetchall()
    difficulty = [item[0] for item in res]
    cursor.execute("SELECT val FROM quality WHERE pid=?", (pid, ))
    res = cursor.fetchall()
    quality = [item[0] for item in res]

    difficulty1 = sum(difficulty) / len(difficulty) if len(difficulty) > 0 else None
    quality1 = sum(quality) / len(quality) if len(quality) > 0 else None
    difficulty2 = np.median(np.array(difficulty)) if len(difficulty) > 0 else None
    quality2 = np.median(np.array(quality)) if len(quality) > 0 else None

    if difficulty1 is None:
        cursor.execute("UPDATE problems SET difficulty=null WHERE pid=?", (pid, ))
    else:
        cursor.execute("UPDATE problems SET difficulty=? WHERE pid=?", (difficulty1, pid))
        
    if difficulty2 is None:
        cursor.execute("UPDATE problems SET difficulty2=null WHERE pid=?", (pid, ))
    else:
        cursor.execute("UPDATE problems SET difficulty2=? WHERE pid=?", (difficulty2, pid))
        
    if quality1 is None:
        cursor.execute("UPDATE problems SET quality=null WHERE pid=?", (pid, ))
    else:
        cursor.execute("UPDATE problems SET quality=? WHERE pid=?", (quality1, pid))
        
    if quality2 is None:
        cursor.execute("UPDATE problems SET quality2=null WHERE pid=?", (pid, ))
    else:
        cursor.execute("UPDATE problems SET quality2=? WHERE pid=?", (quality2, pid))

    cursor.execute("UPDATE problems SET cnt1=?, cnt2=? WHERE pid=?", (len(difficulty), len(quality), pid))
    conn.commit()
    conn.close()

@backend_bp.route('/vote/', methods=['POST'])
def vote():
    if not check_login(request.cookies.get('id')):
        return ""
    if request.form.get("pid") == None:
        return ""
    
    difficulty = int(request.form.get("difficulty"))
    quality = int(request.form.get("quality"))
    comment = request.form.get("comment")
    pid = int(request.form.get("pid"))

    ratingId = random_string(128)

    if difficulty == -1 or (800 <= difficulty and difficulty <= 3500):
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM difficulty WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if res.fetchone() is not None:
            cursor.execute("DELETE FROM difficulty WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if difficulty != -1:
            cursor.execute("INSERT INTO difficulty (username, pid, val, id) VALUES (?,?,?,?)", (get_username(request.cookies.get('id')), pid, difficulty, ratingId))
        conn.commit()
        conn.close()
    
    if quality == -1 or (1 <= quality and quality <= 5):
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM quality WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if res.fetchone() is not None:
            cursor.execute("DELETE FROM quality WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if quality != -1:
            cursor.execute("INSERT INTO quality (username, pid, val, id) VALUES (?,?,?,?)", (get_username(request.cookies.get('id')), pid, quality, ratingId))
        conn.commit()
        conn.close()
    
    if len(comment) <= 500:
        conn = connect_db()
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM comment WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if res.fetchone() is not None:
            cursor.execute("DELETE FROM comment WHERE username=? AND pid=?", (get_username(request.cookies.get('id')), pid))
        if len(comment) != "":
            cursor.execute("INSERT INTO comment (username, pid, val, id) VALUES (?,?,?,?)", (get_username(request.cookies.get('id')), pid, comment, ratingId))
        conn.commit()
        conn.close()
    
    update_rating(pid)

    return ""

@backend_bp.route('/get_vote/', methods=['POST'])
def get_vote():
    if not check_login(request.cookies.get('id')):
        return ""
    if request.form.get("pid") == None:
        return ""
    pid = int(request.form.get("pid"))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM difficulty WHERE pid=? AND username=?", (pid, get_username(request.cookies.get('id'))))
    difficulty = cursor.fetchone()
    cursor.execute("SELECT val FROM quality WHERE pid=? AND username=?", (pid, get_username(request.cookies.get('id'))))
    quality = cursor.fetchone()
    cursor.execute("SELECT val FROM comment WHERE pid=? AND username=?", (pid, get_username(request.cookies.get('id'))))
    comment = cursor.fetchone()
    conn.close()
    if difficulty is None:
        difficulty = 0
    else:
        difficulty = difficulty[0]
    if quality is None:
        quality = 0
    else:
        quality = quality[0]
    if comment is None:
        comment = ""
    else:
        comment = comment[0]
    res = {
        "difficulty": difficulty,
        "quality": quality,
        "comment": comment
    }
    return json.dumps(res), 200, {"Content-Type": "application/json"}

@backend_bp.route('/get_votes/', methods=['POST'])
def get_votes():
    if request.form.get("pid") == None:
        return ""
    pid = int(request.form.get("pid"))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, val, id FROM difficulty WHERE pid=?", (pid, ))
    difficulty = cursor.fetchall()
    cursor.execute("SELECT username, val, id FROM quality WHERE pid=?", (pid, ))
    quality = cursor.fetchall()
    cursor.execute("SELECT username, val, id FROM comment WHERE pid=?", (pid, ))
    comment = cursor.fetchall()

    rating = {}
    for i in range(len(difficulty)):
        if rating.get(difficulty[i][0]) is None:
            rating[difficulty[i][0]] = {"difficulty": None, "quality": None, "comment": None, "id": None}
        rating[difficulty[i][0]]["difficulty"] = difficulty[i][1]
        rating[difficulty[i][0]]["id"] = difficulty[i][2]
    for i in range(len(quality)):
        if rating.get(quality[i][0]) is None:
            rating[difficulty[i][0]] = {"difficulty": None, "quality": None, "comment": None, "id": None}
        rating[quality[i][0]]["quality"] = quality[i][1]
        rating[quality[i][0]]["id"] = quality[i][2]
    for i in range(len(comment)):
        if rating.get(comment[i][0]) is None:
            rating[difficulty[i][0]] = {"difficulty": None, "quality": None, "comment": None, "id": None}
        rating[comment[i][0]]["comment"] = comment[i][1]
        rating[comment[i][0]]["id"] = comment[i][2]
    
    res = []
    for i in rating:
        res.append({
            "difficulty": rating[i]["difficulty"],
            "quality": rating[i]["quality"],
            "comment": rating[i]["comment"],
            "id": rating[i]["id"]
        })

    return json.dumps(res), 200, {"Content-Type": "application/json"}

@backend_bp.route('/report/', methods=['POST'])
def report():
    if not check_login(request.cookies.get('id')):
        return ""
    if request.form.get("id") == None:
        return ""
    username = None
    difficulty = None
    quality = None
    comment = None
    pid = None

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, val, pid FROM difficulty WHERE id=?", (request.form.get("id"), ))
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        difficulty = res[1]
        pid = res[2]
    cursor.execute("SELECT username, val, pid FROM quality WHERE id=?", (request.form.get("id"), ))
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        quality = res[1]
        pid = res[2]
    cursor.execute("SELECT username, val, pid FROM comment WHERE id=?", (request.form.get("id"), ))
    res = cursor.fetchone()
    if res is not None:
        username = res[0]
        comment = res[1]
        pid = res[2]
    conn.close()

    if username is None:
        return ""

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO report (username, pid, difficulty, quality, comment, id) VALUES (?,?,?,?,?,?)", (username, pid, difficulty, quality, comment, request.form.get("id")))
    conn.commit()
    conn.close()

    return ""
    
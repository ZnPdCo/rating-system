from flask import Flask, render_template

app = Flask(__name__)
title = 'Rating System'

@app.route('/')
def index():
    return render_template('index.html', title=title)

@app.route('/login/')
def login():
    return render_template('login.html', title=title)

@app.route('/legal/')
def legal():
    return render_template('legal.html', title=title)
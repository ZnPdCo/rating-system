from flask import Flask, render_template, request, make_response, current_app
import sqlite3 as sl
import hashlib
import random
import string
import json
import numpy as np
from database import connect_db
from utils import check_login, check_admin, get_username, random_string
from main.routes import main_bp
from auth.routes import auth_bp
from admin.routes import admin_bp
from backend.routes import backend_bp

app = Flask(__name__)
app.config['TITLE'] = 'Rating System'

app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin/')
app.register_blueprint(backend_bp, url_prefix='/backend/')


"""
Filename: app.py
Author: ZnPdCo
"""

import json
from flask import Flask, request
from app.main.routes import main_bp
from app.auth.routes import auth_bp
from app.admin.routes import admin_bp
from app.backend.routes import backend_bp
from app.utils import check_login, check_admin

app = Flask(__name__)

app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(admin_bp, url_prefix="/admin/")
app.register_blueprint(backend_bp, url_prefix="/backend/")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


@app.context_processor
def inject_globals():
    """
    Injects global variables to all templates
    """
    with open("i18n/" + config["language"] + ".json", "r", encoding="utf-8") as fp:
        text = json.load(fp)
    return {
        "title": config["title"],
        "logged_in": check_login(request.cookies.get("id")),
        "is_admin": check_admin(request.cookies.get("id")),
        "text": text,
        "oj_name": config["oj_name"],
        "auto_status": config["auto_status"],
    }

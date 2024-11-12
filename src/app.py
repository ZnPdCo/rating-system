"""
Filename: app.py
Author: ZnPdCo
"""

from flask import Flask, request
from main.routes import main_bp
from auth.routes import auth_bp
from admin.routes import admin_bp
from backend.routes import backend_bp
from utils import check_login, check_admin

app = Flask(__name__)

app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(admin_bp, url_prefix="/admin/")
app.register_blueprint(backend_bp, url_prefix="/backend/")


@app.context_processor
def inject_globals():
    """
    Injects global variables to all templates
    """
    return {
        "title": "Rating System",
        "logged_in": check_login(request.cookies.get("id")),
        "is_admin": check_admin(request.cookies.get("id")),
    }

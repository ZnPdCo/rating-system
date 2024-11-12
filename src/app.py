"""
Filename: app.py
Author: ZnPdCo
"""

from flask import Flask
from main.routes import main_bp
from auth.routes import auth_bp
from admin.routes import admin_bp
from backend.routes import backend_bp

app = Flask(__name__)
app.config["TITLE"] = "Rating System"

app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(admin_bp, url_prefix="/admin/")
app.register_blueprint(backend_bp, url_prefix="/backend/")

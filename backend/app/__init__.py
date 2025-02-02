"""
Filename: __init__.py
Author: ZnPdCo
"""

import json
from flask import Flask, request, send_file
from app.main.routes import main_bp
from app.auth.routes import auth_bp
from app.admin.routes import admin_bp
from app.backend.routes import backend_bp
from app.utils import check_login, check_admin
from app.config import config

DIR_PATH_BASE = "../../frontend/"


class WanmaitFlask(Flask):
    """
    Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
    """

    jinja_options = Flask.jinja_options.copy()
    jinja_options.update({"variable_start_string": "%%", "variable_end_string": "%%"})


app = WanmaitFlask(
    __name__,
    static_folder=DIR_PATH_BASE + "dist/assets",
    template_folder=DIR_PATH_BASE + "dist",
)

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
        "title": config["title"],
        "logged_in": check_login(request.cookies.get("id")),
        "is_admin": check_admin(request.cookies.get("id")),
        "oj_name": config["oj_name"],
        "contact": config["contact"],
        "auto_status": config["auto_status"],
    }


@app.route("/favicon.ico", methods=["GET"])
def favicon_route():
    """
    `/favicon.ico` route to serve the favicon
    """
    return send_file(DIR_PATH_BASE + "dist/favicon.ico")

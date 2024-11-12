"""
Filename: main/routes.py
Author: ZnPdCo
"""

from flask import render_template, request, Blueprint, current_app
from utils import check_login, check_admin

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """
    The problems page of the website.
    """
    return render_template(
        "index.html",
        title=current_app.config["TITLE"],
        logged_in=check_login(request.cookies.get("id")),
        is_admin=check_admin(request.cookies.get("id")),
    )


@main_bp.route("/legal/", methods=["GET"])
def legal():
    """
    The legal page of the website.
    """
    return render_template(
        "legal.html",
        title=current_app.config["TITLE"],
        logged_in=check_login(request.cookies.get("id")),
        is_admin=check_admin(request.cookies.get("id")),
    )

"""
Filename: main/routes.py
Author: ZnPdCo
"""

from flask import render_template, Blueprint

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """
    The problems page of the website.
    """
    return render_template(
        "index.html",
    )


@main_bp.route("/legal/", methods=["GET"])
def legal():
    """
    The legal page of the website.
    """
    return render_template(
        "legal.html",
    )

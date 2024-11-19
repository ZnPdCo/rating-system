"""
Filename: main/routes.py
Author: ZnPdCo
"""

import json
from flask import render_template, Blueprint
from app.config import config

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index_route():
    """
    The problems page of the website.
    """
    return render_template(
        "index.html",
    )


@main_bp.route("/legal/", methods=["GET"])
def legal_route():
    """
    The legal page of the website.
    """
    return render_template(
        "index.html",
    )

@main_bp.route("/title/", methods=["GET"])
def title_route():
    """
    The title page of the website.
    """
    return json.dumps({"title": config["title"]}), 200, {"Content-Type": "application/json"}

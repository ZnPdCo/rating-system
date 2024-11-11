from flask import Flask, render_template, request, make_response, Blueprint, current_app
from utils import check_login, check_admin

view = Blueprint('view', __name__)

@view.route('/legal/', methods=['GET'])
def legal():
    return render_template('legal.html', title=current_app.config['TITLE'], logged_in=check_login(request.cookies.get('id')), is_admin=check_admin(request.cookies.get('id')))

"""
this blueprint is aim for test the connection between frontend and backend
and check password and username
"""

from flask import Blueprint
from src.tools.check_login import check_login


index_blue = Blueprint('index', __name__)

# index page 
@index_blue.route('/', methods=['GET'])
@check_login
def index_func(user_id):
    return "Welcome to ElmShow you are login with user "# + str(user_id)
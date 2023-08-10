from flask import Blueprint
from src.tools.check_login import check_login


index_blue = Blueprint('index', __name__)

@index_blue.route('/', methods=['GET'])
@check_login
def index_func(user_id):
    return "Welcome to ElmShow user " + str(user_id)
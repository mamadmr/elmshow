from flask import Blueprint

index_blue = Blueprint('index', __name__)

@index_blue.route('/', methods=['GET'])
def index_func():
    return "Welcome to ElmShow"
from flask import Blueprint
from src.tools.check_login import check_login
from src.database.connector import mysql


get_question_blue = Blueprint('get_question', __name__)

@get_question_blue.route('/get_question', methods=['POST'])
@check_login
def get_question_func(user_id):
    pass

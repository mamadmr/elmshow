from flask import Blueprint
from src.tools.check_login import check_login
from src.tools.check_team import check_team, get_money, get_name
from src.tools.team_requests import get_all_questions
from src.tools.check_storage import get_storage_question
from src.database.connector import run_sql
from flask import current_app
import random
import datetime

from flask import request

bank_blue = Blueprint('bank', __name__)

@bank_blue.route('/bank', methods=['GET'])
@check_login
def enter_score_func(user_id):
    # get all items in bank that can be sold
    questions = run_sql("""SELECT id, question_id, price FROM Bank WHERE status = 1 AND question_id IS NOT NULL""")
    answers = run_sql("""SELECT id, answer_id, price FROM Bank WHERE status = 1 AND answer_id IS NOT NULL""")
    # get questions corresponding to each answer
    output = []
    for answer in answers:
        answer_id = answer[1]
        question_id = run_sql(f"""SELECT question_id FROM Answers WHERE id = {answer_id}""")[0][0]
        temp = [answer[0], ' answer ', answer[1], answer[2], question_id]
        output.append(temp)
    for question in questions:
        temp = [question[0], 'question', question[1], question[2], ""]
        output.append(temp) 
    return output
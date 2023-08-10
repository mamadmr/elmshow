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

get_question_blue = Blueprint('get_question', __name__)

@get_question_blue.route('/get_question', methods=['POST'])
@check_login
def get_question_func(user_id):
    now = datetime.datetime.now()
    current_time = f'{now.hour}:{now.minute}'
    input_data = request.form.to_dict()
    output_dict = {"message": "", "team_name": ""}
    if "team_id" not in input_data:
        output_dict["message"] = "team_id is missing"
        return output_dict, 400
    team_id = input_data["team_id"]
    if not check_team(team_id):
        output_dict["message"] = "this team does not exist"
        return output_dict, 400
    
    if "subquestion" not in input_data:
        output_dict["message"] = "subquestion is missing"
        return output_dict, 400
    subquestion = input_data["subquestion"]

    team_questions = set(get_all_questions(team_id, subquestion))
    storage_questions = set(get_storage_question(subquestion))
    questions = list(storage_questions - team_questions)

    if len(questions) == 0:
        output_dict["message"] = "no question found"
        return output_dict, 400
    
    if get_money(team_id) < current_app.config['config']['question_price']:
        output_dict["message"] = "not enough money"
        return output_dict, 400
    
    question_id = random.choice(questions)
    output_dict['message'] = "success"
    output_dict['question_id'] = question_id
    output_dict['team_name'] = get_name(team_id)
    # check if we have at most config["total_question"] questions in hand
    response = len(run_sql(f"""SELECT questions_in_hand FROM Teams WHERE id = {team_id}""")[0][0].split(',')) - 1
    if response >= current_app.config['config']['total_question']:
        output_dict["message"] = "too many questions in hand"
        return output_dict, 400
      
    # update the database
    # subtract money from team_id
    run_sql(f"""UPDATE Teams SET money = money - {current_app.config['config']['question_price']} WHERE id = {team_id}""")
    # add question to team questions_in_hand
    run_sql(f"""UPDATE Teams SET questions_in_hand = CONCAT(questions_in_hand, '{question_id},') WHERE id = {team_id}""")
    # add row to Questions 
    run_sql(f"""INSERT INTO Questions (question_id, output_time, output_user_id) 
            VALUES ('{question_id}', '{current_time}', {user_id})""")
    # delete question from Storage
    run_sql(f"""DELETE FROM Storage WHERE question_id = {question_id}""")

    return output_dict, 200


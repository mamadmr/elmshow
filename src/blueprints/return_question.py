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

return_question_blue = Blueprint('return_question', __name__)

@return_question_blue.route('/return_question', methods=['POST'])
@check_login
def return_question_func(user_id):
    '''
        input data should include:
            team_id: int
            question_id: str
        output data should include:
            message: str
            team_name: str
    '''
    # initialize time variable
    now = datetime.datetime.now()
    current_time = f'{now.hour}:{now.minute}'
    
    # get input_data
    input_data = request.form.to_dict()

    # initialize output_dict
    output_dict = {"message": "", "team_name": ""}

    # check if team_id is in input_data
    if "team_id" not in input_data:
        output_dict["message"] = "team_id is missing"
        return output_dict, 400
    # check if team_id is valid
    team_id = input_data["team_id"]
    if not check_team(team_id):
        output_dict["message"] = "this team does not exist"
        return output_dict, 400
    
    # check if question_id is in input_data
    if "question_id" not in input_data:
        output_dict["message"] = "question_id is missing"
        return output_dict, 400
    question_id = input_data["question_id"]

    # check if the question_id in the teams questions_in_hand
    team_questions = run_sql(f""" SELECT questions_in_hand FROM Teams WHERE id = {team_id}""")
    if len(team_questions) == 0:
        output_dict["message"] = "this team does not exist"
        return output_dict, 400
    
    # delete empty string
    team_questions = [i for i in team_questions[0][0].split(',') if i != '']
    
    # check if the question_id in the teams questions_in_hand
    if question_id not in team_questions:
        output_dict["message"] = "the team doesn't have this question"
        return output_dict, 400
    
    # update the database
    # return half of the price
    run_sql(f"""UPDATE Teams SET money = money + {current_app.config['config']['question_price']//2} WHERE id = {team_id}""")
    # delete the question_id from questions_in_hand
    run_sql(f"""UPDATE Teams SET questions_in_hand = REPLACE(questions_in_hand, '{question_id},', '') WHERE id = {team_id}""")
    # add the question_id to questions_backed_without_answer
    run_sql(f"""UPDATE Teams SET questions_backed_without_answer = CONCAT(questions_backed_without_answer, '{question_id},') WHERE id = {team_id}""")
    # update the question_id in Questions
    run_sql(f"""UPDATE Questions SET input_time = '{current_time}', input_user_id = {user_id}, back_type = 2 WHERE question_id = {question_id}""")
    # add the question_id to Storage
    run_sql(f"""INSERT INTO Storage (question_id, time_added) VALUES ({question_id}, '{current_time}')""")
    
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(team_id)

    return output_dict, 200

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

return_question_with_answer_blue = Blueprint('return_question_with_answer', __name__)

@return_question_with_answer_blue.route('/return_question_with_answer', methods=['POST'])
@check_login
def return_question_with_answer_func(user_id):
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
    
    if "question_id" not in input_data:
        output_dict["message"] = "question_id is missing"
        return output_dict, 400
    question_id = input_data["question_id"]

    # check if the question_id in the teams questions_in_hand
    team_questions = run_sql(f""" SELECT questions_in_hand FROM Teams WHERE id = {team_id}""")
    if len(team_questions) == 0:
        output_dict["message"] = "no question found"
        return output_dict, 400
    
    team_questions = [i for i in team_questions[0][0].split(',') if i != '']
    
    if question_id not in team_questions:
        output_dict["message"] = "the team doesn't have this question"
        return output_dict, 400    
    
    # update database
    run_sql(f""" UPDATE Teams SET questions_in_hand = REPLACE(questions_in_hand, '{question_id},', '') WHERE id = {team_id}""")
    run_sql(f""" UPDATE Teams SET questions_backed_with_answer = CONCAT(questions_backed_with_answer, '{question_id},') WHERE id = {team_id}""")
    run_sql(f"""UPDATE Questions SET input_time = '{current_time}', input_user_id = {user_id}, back_type = 1 WHERE question_id = {question_id}""")
    run_sql(f"""INSERT INTO Storage (question_id, time_added) VALUES ({question_id}, '{current_time}')""")
    answers_id = len(run_sql("""SELECT * FROM Answers""")) + 4236
    run_sql(f"""INSERT INTO Answers (id, question_id, team_id, time, user_id) VALUES ({answers_id}, {question_id}, {team_id}, '{current_time}', {user_id})""")
    run_sql(f"""UPDATE Teams SET answers_to_check = CONCAT(answers_to_check, '{answers_id},') WHERE id = {team_id}""")
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(team_id)
    output_dict['answer_id'] = answers_id 
    return output_dict, 200

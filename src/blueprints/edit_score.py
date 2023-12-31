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

edit_score_blue = Blueprint('edit_score', __name__)

@edit_score_blue.route('/edit_score', methods=['POST'])
@check_login
def edit_score_func(user_id):
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
    
    if "answer_id" not in input_data:
        output_dict["message"] = "answer_id is missing"
        return output_dict, 400
    answer_id = input_data["answer_id"]

    # check for score in header 
    if 'score' not in input_data:
        output_dict["message"] = "score is missing"
        return output_dict, 400
    score = input_data['score']

    # check for sellable in header
    if 'sellable' not in input_data:
        output_dict["message"] = "sellable is missing"
        return output_dict, 400
    sellable = input_data['sellable']
    # check if the answer is for this team
    if str(answer_id) not in run_sql(f""" SELECT answers_checked FROM Teams WHERE id = {team_id}""")[0][0].split(','):
        output_dict["message"] = "team does not have this answer"
        return output_dict, 400

    # check if the answer_id in the teams answers_checked
    team_answers = run_sql(f""" SELECT answers_checked FROM Teams WHERE id = {team_id}""")
    if len(team_answers) == 0:
        output_dict["message"] = "no answer found"
        return output_dict, 400
    # get old score 
    old_score = run_sql(f""" SELECT score FROM Answers WHERE id = {answer_id}""")[0][0]
    diff_score = int(score) - int(old_score)
    # update database
    run_sql(f""" UPDATE Teams SET score = score + {diff_score} WHERE id = {team_id}""")
    run_sql(f"""UPDATE Answers SET user_id_check = {user_id}, time_check = '{current_time}', score = {score}, is_sellable = {sellable} WHERE id = {answer_id}""")

    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(team_id)
    return output_dict, 200
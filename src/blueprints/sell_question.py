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

sell_question_blue = Blueprint('sell_question', __name__)

@sell_question_blue.route('/sell_question', methods=['POST'])
@check_login
def sell_question_func(user_id):
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

    if "price" not in input_data:
        output_dict["message"] = "price is missing"
        return output_dict, 400
    price = input_data["price"]

    # check if the question_id in the teams questions_in_hand
    team_questions = run_sql(f""" SELECT questions_in_hand FROM Teams WHERE id = {team_id}""")[0][0].split(',')
    if question_id not in team_questions:
        output_dict["message"] = "team doesn't have this question"
        return output_dict, 400
    
    # check if the question_id not in bought questions 
    bought_questions = run_sql(f""" SELECT questions_bought FROM Teams WHERE id = {team_id}""")[0][0].split(',')
    if question_id in bought_questions:
        output_dict["message"] = "team already bought this question"
        return output_dict, 400

    # check if question_to_sell is less than config[total_question_in_bank]
    in_bank = run_sql(f"""SELECT questions_to_sell FROM Teams WHERE id= {team_id}""")[0][0].split(',')
    in_bank = [i for i in in_bank if i != '']
    if len(in_bank) >= current_app.config['config']["total_question_in_bank"]:
        output_dict['message'] = 'you have many questions in bank'
        return output_dict, 400

    # update database
    run_sql(f""" UPDATE Teams SET questions_in_hand = REPLACE(questions_in_hand, '{question_id},', '') WHERE id = {team_id}""")
    run_sql(f""" UPDATE Teams SET questions_to_sell = CONCAT(questions_to_sell, '{question_id},') WHERE id = {team_id}""")
    run_sql(f""" INSERT Bank 
            (question_id, team_seller_id, input_time, user_id_add_to_bank, price, changes, status)
            VALUES 
            ({question_id}, {team_id}, '{current_time}', {user_id}, {price}, '', 1)""")
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(team_id)

    return output_dict, 200



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

sell_answer_blue = Blueprint('sell_answer', __name__)

@sell_answer_blue.route('/sell_answer', methods=['POST'])
@check_login
def sell_answer_func(user_id):
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

    if "price" not in input_data:
        output_dict["message"] = "price is missing"
        return output_dict, 400
    price = input_data["price"]

    # check if the team has this answer
    all_answers = run_sql(f""" SELECT answers_checked FROM Teams WHERE id = {team_id}""")[0][0].split(',')
    if str(answer_id) not in all_answers:
        output_dict["message"] = "team does not have this answer"
        return output_dict, 400
    
    # check if the answer is not sold before
    if len(run_sql(f""" SELECT id FROM Bank WHERE answer_id = {answer_id}""")) != 0:
        output_dict["message"] = "this answer is already sold"
        return output_dict, 400
    
    # check if the answer is_sellable 
    if run_sql(f""" SELECT is_sellable FROM Answers WHERE id = {answer_id}""")[0][0] != 1:
        output_dict["message"] = "this answer is not sellable"
        return output_dict, 400
    
    # check if the team doesn't buy this answer before
    if str(answer_id) in run_sql(f""" SELECT answers_bought FROM Teams WHERE id = {team_id}""")[0][0].split(','):
        output_dict["message"] = "team already bought this answer"
        return output_dict, 400
    
    # update database
    # add to bank
    run_sql(f""" INSERT INTO Bank (answer_id, team_seller_id, input_time, user_id_add_to_bank, price, changes, status) 
            VALUES ({answer_id}, {team_id}, '{current_time}', {user_id}, {price}, '', 1)""")
    
    # add answer to answers_to_sell
    run_sql(f""" UPDATE Teams SET answers_to_sell = CONCAT(answers_to_sell, '{answer_id},') WHERE id = {team_id}""")

    output_dict["message"] = "success"
    output_dict["team_name"] = get_name(team_id)

    return output_dict, 200
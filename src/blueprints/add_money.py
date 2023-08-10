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

add_money_blue = Blueprint('add_money', __name__)

@add_money_blue.route('/add_money', methods=['POST'])
@check_login
def add_money_func(user_id):
    now = datetime.datetime.now()
    current_time = f'{now.hour}:{now.minute}'
    input_data = request.form.to_dict()
    output_dict = {"message": "", "team_name": "", "money": 0}

    if "team_id" not in input_data:
        output_dict["message"] = "team_id is missing"
        return output_dict, 400
    
    team_id = input_data["team_id"]
    if not check_team(team_id):
        output_dict["message"] = "this team does not exist"
        return output_dict, 400
    
    amount = 0
    if 'amount' in input_data:
        amount = int(input_data['amount']) 

    # update database
    run_sql(f""" UPDATE Teams SET money = money + {amount} WHERE id = {team_id}""")
    run_sql(f""" INSERT AmusementPark (user_id, time, money_added) VALUES ({user_id}, '{current_time}', {amount})""") 
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(team_id)
    output_dict['money'] = run_sql(f""" SELECT money FROM Teams WHERE id = {team_id}""")[0][0]
    return output_dict, 200
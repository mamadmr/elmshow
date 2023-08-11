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

update_price_blue = Blueprint('update_price', __name__)

@update_price_blue.route('/update_price', methods=['POST'])
@check_login
def update_price_func(user_id):
    now = datetime.datetime.now()
    current_time = f'{now.hour}:{now.minute}'
    input_data = request.form.to_dict()
    output_dict = {"message": "", "team_name": ""}

    if 'bank_id' not in input_data:
        output_dict["message"] = "bank_id is missing"
        return output_dict, 400
    bank_id = input_data['bank_id']

    if 'price' not in input_data:
        output_dict["message"] = "price is missing"
        return output_dict, 400
    new_price = input_data['price']

    if 'team_id' not in input_data:
        output_dict["message"] = "team_id is missing"
        return output_dict, 400
    team_id = input_data['team_id']

    # check if the item exists in bank 
    if len(run_sql(f""" SELECT id FROM Bank WHERE id = {bank_id}""")) == 0:
        output_dict["message"] = "this item is not in bank"
        return output_dict, 400

    team_id_bank = run_sql(f""" SELECT team_seller_id FROM Bank WHERE id = {bank_id}""")[0][0]
    old_price = run_sql(f""" SELECT price FROM Bank WHERE id = {bank_id}""")[0][0]

    # check if the team is the owner of the bank
    if int(team_id_bank) != int(team_id):
        output_dict["message"] = "this team is not the owner of this bank"
        return output_dict, 400
    
    # check if the item is not sold
    if run_sql(f""" SELECT status FROM Bank WHERE id = {bank_id}""")[0][0] != 1:
        output_dict["message"] = "this item is not for sale"
        return output_dict, 400
    
    # update database 
    run_sql(f""" UPDATE Bank SET price = {new_price} WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET changes = CONCAT(changes, '{(user_id, old_price)},') WHERE id = {bank_id}""")

    output_dict["message"] = "success"
    output_dict["team_name"] = get_name(team_id)
    
    return output_dict, 200
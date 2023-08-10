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

buy_question_blue = Blueprint('buy_question', __name__)

@buy_question_blue.route('/buy_question', methods=['POST'])
@check_login
def get_question_func(user_id):
    now = datetime.datetime.now()
    current_time = f'{now.hour}:{now.minute}'
    input_data = request.form.to_dict()
    output_dict = {"message": "", "team_name": ""}

    if 'bank_id' not in input_data:
        output_dict["message"] = "bank_id is missing"
        return output_dict, 400
    bank_id = input_data['bank_id']

    if 'team_id' not in input_data:
        output_dict["message"] = "team_id is missing"
        return output_dict, 400
    buyer_id = input_data["team_id"]

    seller_id = run_sql(f""" SELECT team_seller_id FROM Bank WHERE id = {bank_id}""")[0][0]
    subquestion = str(run_sql(f""" SELECT question_id FROM Bank WHERE id = {bank_id}""")[0][0])[:current_app.config['config']["sub_len"]]
    price = run_sql(f""" SELECT price FROM Bank WHERE id = {bank_id}""")[0][0]

    # check if the team hasn't got this question before
    team_questions = list(get_all_questions(buyer_id, subquestion))
    check = [i for i in team_questions if i.startswith(subquestion)]
    if len(check) < 0:
        output_dict["message"] = "team already has this question"
        return output_dict, 400 
    
    # check if the bank_id in the bank to sell 
    if len(run_sql(f""" SELECT question_id FROM Bank WHERE id = {bank_id}""")) == 0:
        output_dict["message"] = "this item is not in bank"
        return output_dict, 400

    # it's not sold
    if run_sql(f""" SELECT status FROM Bank WHERE id = {bank_id}""")[0][0] != 1:
        output_dict["message"] = "this item is not for sale"
        return output_dict, 400
    # it's a question 
    if len(str(run_sql(f""" SELECT question_id FROM Bank WHERE id = {bank_id}""")[0][0])) <= current_app.config['config']["sub_len"]: 
        output_dict["message"] = "this item is not a question"
        return output_dict, 400

    # check if team has enough money
    if get_money(buyer_id) < price:
        output_dict["message"] = "not enough money"
        return output_dict, 400
    
    # check if we have at most config["total_question"] questions in hand
    response = len([i for i in run_sql(f"""SELECT questions_in_hand FROM Teams WHERE id = {buyer_id}""")[0][0].split(',') if i != ''])
    if response >= current_app.config['config']['total_question']:
        output_dict["message"] = "too many questions in hand"
        return output_dict, 400
    

    # get question_id
    question_id = run_sql(f""" SELECT question_id FROM Bank WHERE id = {bank_id}""")[0][0]

    # update database
    # update buyer
    run_sql(f""" UPDATE Teams SET questions_in_hand = CONCAT(questions_in_hand, '{question_id},') WHERE id = {buyer_id}""")
    run_sql(f""" UPDATE Teams SET questions_bought = CONCAT(questions_bought, '{question_id},') WHERE id = {buyer_id}""")
    run_sql(f""" UPDATE Teams SET money = money - {price} WHERE id = {buyer_id}""")
    # update seller
    run_sql(f""" UPDATE Teams SET money = money + {price} WHERE id = {seller_id}""")
    run_sql(f""" UPDATE Teams SET questions_sold = CONCAT(questions_sold, '{question_id},') WHERE id = {seller_id}""")
    run_sql(f""" UPDATE Teams SET questions_to_sell = REPLACE(questions_to_sell, '{question_id},', '') WHERE id = {seller_id}""")
    # update bank
    run_sql(f""" UPDATE Bank SET team_buyer_id = {buyer_id} WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET output_time = '{current_time}' WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET user_id_remove_from_bank = {user_id} WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET status = 2 WHERE id = {bank_id}""")
    
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(buyer_id)

    return output_dict, 200




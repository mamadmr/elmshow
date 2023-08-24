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

buy_answer_blue = Blueprint('buy_answer', __name__)

@buy_answer_blue.route('/buy_answer', methods=['POST'])
@check_login
def buy_answer_func(user_id):
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

    # check if the item exists in bank 
    if len(run_sql(f""" SELECT id FROM Bank WHERE id = {bank_id}""")) == 0:
        output_dict["message"] = "this item is not in bank"
        return output_dict, 400
    
    # check if the item is a answer
    if len(str(run_sql(f""" SELECT answer_id FROM Bank WHERE id = {bank_id}""")[0][0])) <= 1:
        output_dict["message"] = "this item is not a answer"
        return output_dict, 400
    
    

    seller_id = run_sql(f""" SELECT team_seller_id FROM Bank WHERE id = {bank_id}""")[0][0]
    answer_id = str(run_sql(f""" SELECT answer_id FROM Bank WHERE id = {bank_id}""")[0][0])
    price = run_sql(f""" SELECT price FROM Bank WHERE id = {bank_id}""")[0][0]


    # get the question_id of this answer
    question_id = run_sql(f""" SELECT question_id FROM Answers WHERE id = {answer_id}""")[0][0]
    subquestion = str(question_id)[:current_app.config['config']["sub_len"]]

    # check if the team has the question of this answer in hand
    questions_in_hand = run_sql(f""" SELECT questions_in_hand FROM Teams WHERE id = {buyer_id}""")[0][0].split(',')
    check = [i for i in questions_in_hand if i.startswith(subquestion)]
    if len(check) == 0:
        output_dict["message"] = "team does not have this question"
        return output_dict, 400
    

    # it's not sold
    if run_sql(f""" SELECT status FROM Bank WHERE id = {bank_id}""")[0][0] != 1:
        output_dict["message"] = "this item is not for sale"
        return output_dict, 400

    # check if team has enough money
    if get_money(buyer_id) < price:
        output_dict["message"] = "not enough money"
        return output_dict, 400
    
    

    # update database 
    # update seller
    run_sql(f""" UPDATE Teams SET answers_sold = CONCAT(answers_sold, '{answer_id},') WHERE id = {seller_id}""")
    run_sql(f""" UPDATE Teams SET money = money + {price} WHERE id = {seller_id}""")
    run_sql(f""" UPDATE Teams SET answers_to_sell = REPLACE(answers_to_sell, '{answer_id},', '') WHERE id = {seller_id}""")

    # update buyer
    run_sql(f""" UPDATE Teams SET answers_bought = CONCAT(answers_bought, '{answer_id},') WHERE id = {buyer_id}""")
    run_sql(f""" UPDATE Teams SET money = money - {price} WHERE id = {buyer_id}""")

    # update bank
    run_sql(f""" UPDATE Bank SET team_buyer_id = {buyer_id} WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET output_time = '{current_time}' WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET user_id_remove_from_bank = {user_id} WHERE id = {bank_id}""")
    run_sql(f""" UPDATE Bank SET status = 2 WHERE id = {bank_id}""")
    
    output_dict['message'] = "success"
    output_dict['team_name'] = get_name(buyer_id)

    return output_dict, 200




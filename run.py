from flask import Flask
import json

# read config file 
with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.app_context().push()

# set config
app.config['config'] = config

# import blueprints
from src.blueprints.index import index_blue
from src.blueprints.get_question_from_storage import get_question_blue
from src.blueprints.return_question import return_question_blue
from src.blueprints.return_question_with_answer import return_question_with_answer_blue
from src.blueprints.enter_score import enter_score_blue
from src.blueprints.edit_score import edit_score_blue
from src.blueprints.add_money import add_money_blue 
from src.blueprints.sell_question import sell_question_blue
from src.blueprints.buy_question import buy_question_blue
from src.blueprints.update_price import update_price_blue   
from src.blueprints.sell_answer import sell_answer_blue

# register blueprints
app.register_blueprint(index_blue)
app.register_blueprint(get_question_blue)
app.register_blueprint(return_question_blue)
app.register_blueprint(return_question_with_answer_blue)
app.register_blueprint(enter_score_blue)
app.register_blueprint(edit_score_blue)
app.register_blueprint(add_money_blue)
app.register_blueprint(sell_question_blue)
app.register_blueprint(buy_question_blue)
app.register_blueprint(update_price_blue)
app.register_blueprint(sell_answer_blue)

if __name__ == '__main__':
    app.run(debug=True)
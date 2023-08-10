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

# register blueprints
app.register_blueprint(index_blue)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)
app.app_context().push()

# import blueprints
from src.blueprints.index import index_blue

# register blueprints
app.register_blueprint(index_blue)



if __name__ == '__main__':
    app.run(debug=True)
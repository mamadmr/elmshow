from functools import wraps
from flask import request
from flask import jsonify
import src.database.connector as connector

def check_login(func):
    """
    this function check for password and username in the header of the request 
    needed headers 
        - username
        - password
    """

    # use wraps to keep the original function name
    @wraps(func)
    def decorator():
        token = None
        output_dict = dict()

        # check if the username and password are passed with the headers
        if 'username'  not in request.headers:
            output_dict['error'] = 'Username is missing!'
            return jsonify(output_dict), 401 
        
        if 'password' not in request.headers:
            output_dict['error'] = 'Password is missing!'
            return jsonify(output_dict), 401

        # get user id from user name and password
        user = connector.run_sql(f'SELECT id FROM Users WHERE username = "{request.headers["username"]}" AND password = "{request.headers["password"]}"')
        if len(user) == 0:
            output_dict['error'] = 'Username or password is incorrect!'
            return jsonify(output_dict), 401

        return func(user[0][0])
        
    return decorator
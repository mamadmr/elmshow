import src.database.connector as connector


def check_team(team_id):
    # check if team_id is in database
    sql = f'SELECT * FROM Teams WHERE id = {team_id}'
    result = connector.run_sql(sql)
    if len(result) == 0:
        return False
    return True

def get_money(team_id):
    # get the money of the team with team_id
    result = connector.run_sql(f"""SELECT money FROM Teams WHERE id = {team_id}""")
    return result[0][0]

def get_name(team_id):
    # get the name of the team with team_id
    result = connector.run_sql(f"""SELECT name FROM Teams WHERE id = {team_id}""")
    return result[0][0]
import src.database.connector as connector


def get_all_questions(team_id, subquestion):
    # get all the subquestion of the team with team_id
    result = connector.run_sql(f"""SELECT 
                        questions_in_hand,
                        questions_backed_with_answer,
                        questions_backed_without_answer,
                        questions_to_sell,
                        questions_sold,
                        questions_bought
                       FROM Teams WHERE id = {team_id}""")

    return [i.strip() for i in (','.join(result[0]).split(',')) if i != '' and i.startswith(subquestion)]

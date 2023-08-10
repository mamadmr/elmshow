import src.database.connector as connector


def get_storage_question(subquestion):
    # get all the questions that starts with subquestion
    result = connector.run_sql(f"""SELECT question_id FROM Storage""")
    return [str(i[0]) for i in result if str(i[0]).startswith(subquestion)]

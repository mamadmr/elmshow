import connector


add_users = True
add_teams = True
add_to_storage = True

# add 13 new users and 1 admin to the database
if add_users:
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('admin', 'admin', 'admin')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user1', 'user1', 'user1')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user2', 'user2', 'user2')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user3', 'user3', 'user3')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user4', 'user4', 'user4')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user5', 'user5', 'user5')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user6', 'user6', 'user6')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user7', 'user7', 'user7')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user8', 'user8', 'user8')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user9', 'user9', 'user9')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user10', 'user10', 'user10')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user11', 'user11', 'user11')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user12', 'user12', 'user12')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user13', 'user13', 'user13')""")


# add 22 new teams to the database
if add_teams:
    connector.run_sql("""INSERT INTO Teams (id, name, money, score, questions_in_hand, questions_backed_with_answer, questions_backed_without_answer, questions_to_sell, questions_sold, questions_bought, answers_to_check, answers_checked, answers_to_sell, answers_sold, answers_bought)
                    VALUE 
                      (1, 'team1', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (2, 'team2', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (3, 'team3', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (4, 'team4', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (5, 'team5', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (6, 'team6', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (7, 'team7', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (8, 'team8', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (9, 'team9', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (10, 'team10', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (11, 'team11', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (12, 'team12', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (13, 'team13', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (14, 'team14', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (15, 'team15', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (16, 'team16', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (17, 'team17', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (18, 'team18', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (19, 'team19', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (20, 'team20', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (21, 'team21', 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (22, 'team22', 1000, 0, '', '', '', '', '', '', '', '', '', '', '');
                      """)


# add 10 new questions to the Storage table
if add_to_storage:
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1111, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1112, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1113, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1114, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1121, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1122, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1123, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1124, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1131, '00:00:00')""")
    connector.run_sql("""INSERT INTO Storage (question_id, time_added) VALUES (1132, '00:00:00')""")

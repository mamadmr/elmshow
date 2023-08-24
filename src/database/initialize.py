import connector


add_users = False
add_teams = False
add_to_storage = False

# add 13 new users and 1 admin to the database
if add_users:
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('admin', 'admin', 'admin')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('amin', 'amin', 'amin')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('Armin Sedaghat', 'arm', 'arm')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('Arefeh', 'arf', 'arf')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('Ali Gitizadeh', 'git', 'git')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('ali dakik', 'dak', 'dak')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('narges toosheh', 'ngs', 'ngs')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('amirhossein khoshnude', 'nude', 'nude')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('anahit pishan', 'ana', 'ana')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('abolfazl gargoori', 'grg', 'grg')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('zhina Eslami', 'zhs', 'zhs')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('fatemeh dashti', 'fd', 'fd')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('homa', 'homa', 'homa')""")
    connector.run_sql("""INSERT INTO Users (name, username, password) VALUES ('user13', 'user13', 'user13')""")


# add 22 new teams to the database
if add_teams:
    connector.run_sql("""INSERT INTO Teams (id, name, money, score, questions_in_hand, questions_backed_with_answer, questions_backed_without_answer, questions_to_sell, questions_sold, questions_bought, answers_to_check, answers_checked, answers_to_sell, answers_sold, answers_bought)
                    VALUE 
                      (1, 'A3+',                        1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (2, 'PES',                        1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (3, 'mottahedin sevom',           1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (4, 'emam',                       1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (5, 'karbalye 4',                 1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (6, 'jange jahanie sevom',        1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (7, 'mohsen',                     1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (8, 'zenith',                     1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (9, 'bajenagh ha',                1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (10, 'jangali',                   1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (11, 'sin jin',                   1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (12, 'mottafeghin sevom',         1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (13, 'meddelin',                  1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (14, 'matilda',                   1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (15, 'kharboze haye khoshhal',    1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (16, 'amigdal',                   1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (17, 'asghardooni',               1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (18, 'bacteri haye geram manfi',  1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (19, 'kakero',                    1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (20, 'zereshk',                   1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (21, 'violet',                    1000, 0, '', '', '', '', '', '', '', '', '', '', ''),
                      (22, 'shayatine sorkh',           1000, 0, '', '', '', '', '', '', '', '', '', '', '');
                      """)


# add 10 new questions to the Storage table
if add_to_storage:
    for i in [1,2,3,4]:
        for j in [1, 2, 3]:
            for t in [1, 2]:
                for k in [1, 2, 3, 4]:
                    code = str(i) + str(j) + str(t) + str(k)
                    connector.run_sql(f"""INSERT INTO Storage (question_id, time_added) VALUES ({code}, '00:00:00')""")


if True:
    for i in [1, 2, 3]:
        for j in [3, 4]:
            for t in [1, 2, 3, 4]:
                code = '4' + str(i) + str(j) + str(t)

    connector.run_sql(f"""INSERT INTO Storage (question_id, time_added) VALUES ({code}, '00:00:00')""")

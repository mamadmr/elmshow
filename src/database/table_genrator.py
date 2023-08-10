import connector

# drop all existing tables
connector.run_sql(""" DROP TABLE IF EXISTS Users, Teams, Questions, Answers, Bank, Storage, AmusementPark;""")

# create all tables
connector.run_sql("""CREATE TABLE Users (
                  id INT NOT NULL AUTO_INCREMENT,
                  PRIMARY KEY (`id`),
                  name VARCHAR(255) NOT NULL,
                  username VARCHAR(100) NOT NULL, 
                  password VARCHAR(100) NOT NULL)
                  """)


connector.run_sql("""CREATE TABLE Teams (
                    id INT NOT NULL,
                    PRIMARY KEY (`id`),
                    name VARCHAR(255) NOT NULL,
                    money INT NOT NULL,
                    score INT NOT NULL,
                    questions_in_hand VARCHAR(500),
                    questions_backed_with_answer VARCHAR(500),
                    questions_backed_without_answer VARCHAR(500),
                    questions_to_sell VARCHAR(500),
                    questions_sold VARCHAR(500),
                    questions_bought VARCHAR(500),
                    answers_to_check VARCHAR(500),
                    answers_checked VARCHAR(500),
                    answers_to_sell VARCHAR(500),
                    answers_sold VARCHAR(500),
                    answers_bought VARCHAR(500)
                  )""")

# back_type
#   1: question_with_answer
#   2: question_without_answer 
connector.run_sql("""CREATE TABLE Questions(
                  id INT NOT NULL,
                  PRIMARY KEY (`id`),
                  question_id INT NOT NULL,
                  output_time VARCHAR(10) NOT NULL,
                  output_user_id INT NOT NULL,
                  input_time VARCHAR(10),
                  input_user_id INT,
                  back_type INT,
                  FOREIGN KEY (output_user_id) REFERENCES Users(id),
                  FOREIGN KEY (input_user_id) REFERENCES Users(id)
)""")


connector.run_sql("""CREATE TABLE Answers(
                    id INT NOT NULL,
                    PRIMARY KEY (`id`),
                    question_id INT NOT NULL,
                    team_id INT NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    score INT NOT NULL,
                    is_sellable INT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES Questions(id),
                    FOREIGN KEY (team_id) REFERENCES Teams(id)
                  )""")               
 
# status 
#  1: waiting to be sold
#  2: sold
connector.run_sql("""CREATE TABLE Bank(
                    id INT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (`id`),
                    question_id INT,
                    answer_id INT, 
                    team_seller_id INT NOT NULL,
                    input_time VARCHAR(10) NOT NULL,
                    user_id_add_to_bank INT NOT NULL,
                    team_buyer_id INT,
                    output_time VARCHAR(10),
                    user_id_remove_from_bank INT,
                    price INT NOT NULL,
                    changes VARCHAR(500) NOT NULL,
                    status INT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES Questions(id),
                    FOREIGN KEY (answer_id) REFERENCES Answers(id),
                    FOREIGN KEY (team_seller_id) REFERENCES Teams(id),
                    FOREIGN KEY (user_id_add_to_bank) REFERENCES Users(id),
                    FOREIGN KEY (team_buyer_id) REFERENCES Teams(id),
                    FOREIGN KEY (user_id_remove_from_bank) REFERENCES Users(id)
                  )""")

connector.run_sql("""CREATE TABLE Storage(
                    id INT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (`id`),
                    question_id INT,
                    time_added VARCHAR(10) NOT NULL
                        )""")

connector.run_sql("""CREATE TABLE AmusementPark(
                    id INT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (`id`),
                    user_id INT NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    money_added INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                  )""")

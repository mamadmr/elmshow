import  mysql.connector

# read config file 
import json
with open('config.json') as json_file:
    config = json.load(json_file)

def run_sql(sql):
    MyDB = mysql.connector.connect(
    host=config["Database_host"],
    user=config["Database_Username"],
    password=config["Database_Password"],
    database=config["Database_name"]
    )    
    MyCursor = MyDB.cursor()
    MyCursor.execute(sql)
    MyResult = MyCursor.fetchall()
    MyDB.commit()
    return MyResult
from psycopg2 import OperationalError, connect
from psycopg2.errors import DuplicateDatabase, DuplicateTable

DB_USER = input('Type your database username: ')
DB_PASSWORD = input('Type your database password: ')
HOST = input('Type HOST: ')

sql_create_db = "CREATE DATABASE messages_db;"
sql_create_table_user = '''CREATE TABLE Users (
    id serial PRIMARY KEY, 
    username varchar(225) UNIQUE,
    hashed_password varchar(80)
);'''
sql_create_table_message = '''CREATE TABLE Message (
    id serial PRIMARY KEY,
    from_id int,
    to_id int,
    creation_date timestamp,
    text varchar(255),
    FOREIGN KEY (from_id) REFERENCES Users(id),
    FOREIGN KEY (to_id) REFERENCES Users(id)
);'''

try:
    create_con = connect(database="postgres", user=DB_USER, password=DB_PASSWORD, host=HOST)
    create_con.autocommit = True
    cursor = create_con.cursor()
    try:
        cursor.execute(sql_create_db)
        print("Database created")
    except DuplicateDatabase as err:
        print("Database already exists: ", err)
    create_con.close()
except OperationalError as err2:
    print("Connection Error: ", err2)

try:
    create_con = connect(database="messages_db", user=DB_USER, password=DB_PASSWORD, host=HOST)
    create_con.autocommit = True
    cursor = create_con.cursor()
    try:
        cursor.execute(sql_create_table_user)
        print('Table "Users" created')
    except DuplicateTable as err:
        print("Table 'Users' already exists: ", err)
    create_con.close()
except OperationalError as err2:
    print("Connection Error: ", err2)

try:
    create_con = connect(database="messages_db", user=DB_USER, password=DB_PASSWORD, host=HOST)
    create_con.autocommit = True
    cursor = create_con.cursor()
    try:
        cursor.execute(sql_create_table_message)
        print('Table "message" created')
    except DuplicateTable as err:
        print("Database 'message'' exists: ", err)
    create_con.close()
except OperationalError as err2:
    print("Connection Error: ", err2)

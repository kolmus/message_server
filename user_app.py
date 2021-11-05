import argparse
from hashlib import new
from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase, OperationalError, UniqueViolation
from models import User, check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

def create_user(username, password):
    create_con = connect(database="messages_db", user='postgres', password='coderslab', host='127.0.0.1')
    create_con.autocommit = True
    cursor = create_con.cursor()
    try:
        new_user = User(username, password)
        new_user.save_to_db(cursor)
        create_con.close()
        return f'User {username} created!'
    except UniqueViolation:
        return f'User {username} already exist!'

def edit_password(username, password, new_pass):
    create_con = connect(database="messages_db", user='postgres', password='coderslab', host='127.0.0.1')
    create_con.autocommit = True
    cursor = create_con.cursor()
    user_new_password = User.load_user_by_username(cursor, username)
    if check_password(password, user_new_password._hashed_password) is True:
        if len(new_pass) < 8:
            create_con.close()
            return "New password is too short. Min 8 charakters."
        else:
            user_new_password.password(new_pass)
            user_new_password.save_to_db(cursor)
            create_con.close()
            return "New password saved."
    else:
        create_con.close()
        return "Authorization failed"

def delete_user(username, password,):
    create_con = connect(database="messages_db", user='postgres', password='coderslab', host='127.0.0.1')
    create_con.autocommit = True
    cursor = create_con.cursor()
    user_del = User.load_user_by_username(cursor, username)
    if check_password(password, user_del._hashed_password) is True:
        user_del.delete(cursor)
        create_con.close()
        return f"User {username} deleted from database"
    else:
        create_con.close()
        return "Authorization failed"

def list_users(username, password):
    create_con = connect(database="messages_db", user='postgres', password='coderslab', host='127.0.0.1')
    create_con.autocommit = True
    cursor = create_con.cursor()
    create_con.close()
    users_list = []
    for user in User.load_all_users(cursor):
        users_list.append(user.username)
    return f"List of users:\n" +',\n'.join(users_list)

def help_for_users():
    parser.print_help()

if args.username != "" and args.password != "":
    if args.delete == True:
        delete_user(args.username, args.password)                    # delete user for -u and -p and -d
    elif args.edit == True and args.new_pass != "":
        edit_password(args.username, args.password, args.new_pass)   # edit pasword for -u and -p and -e and -n
    else:
        create_user(args.username, args.password)                     # create user for -u and -p
elif args.list == True:
    list_users                                                       # list users for -l
else:
    help_for_users                                                   # other arguments in parser
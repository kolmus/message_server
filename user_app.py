import argparse
import psycopg2
import psycopg2.errors
from clcrypto import check_password
from models import User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

def create_user(username, password):
    try:
        new_user = User(username, password)
        new_user.save_to_db(cursor)
        print(f'User {username} created!')
    except psycopg2.errors.UniqueViolation:
        print(f'User {username} already exist!')

def edit_password(username, password, new_pass):
    user_new_password = User.load_user_by_username(cursor, username)
    if check_password(password, user_new_password._hashed_password) is True:
        if len(new_pass) < 8:
            print("New password is too short. Min 8 charakters.")
        else:
            user_new_password.set_password(new_pass)
            user_new_password.save_to_db(cursor)
            print("New password saved.")
    else:
        print("Authorization failed")

def delete_user(username, password,):
    user_del = User.load_user_by_username(cursor, username)
    if check_password(password, user_del._hashed_password) is True:
        user_del.delete(cursor)
        print(f"User {username} deleted from database")
    else:
        print("Authorization failed")

def list_users():
    users_list = []
    for user in User.load_all_users(cursor):
        users_list.append(user.username)
    print(f"List of users:\n" +'\n'.join(users_list))

def help_for_users():
    parser.print_help()

if __name__ == '__main__':
    try:
        create_con = psycopg2.connect(database="messages_db", user='postgres', password='coderslab', host='127.0.0.1')
        create_con.autocommit = True
        cursor = create_con.cursor()
        if args.username is not None and args.password is not None:      # is not None propozycja Pawła na warsztatach, narawia kod. Wcześniej != "" - nie działa
            if args.delete == True:
                delete_user(args.username, args.password)                    # delete user for -u and -p and -d
            elif args.edit == True and args.new_pass is not None:
                edit_password(args.username, args.password, args.new_pass)   # edit pasword for -u and -p and -e and -n
            else:
                create_user(args.username, args.password)                     # create user for -u and -p
        elif args.list == True:
            list_users()                                                       # list users for -l
        else:
            help_for_users                                                   # other arguments in parser
        create_con.close()
    except psycopg2.OperationalError as error:
        print("Connection Error: " + error)

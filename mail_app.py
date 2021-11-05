import argparse
import psycopg2
from models import Message, User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="username you want to send message")
parser.add_argument("-s", "--send", help="content of your message")
parser.add_argument("-l", "--list", help="list all my messages")

args = parser.parse_args()

def list_of_messages(username, cursor):
    message_list = []
    for row in Message.load_all_messages(cursor):
        if row.username == username:
            from_username = User.load_user_by_id(cursor, row.from_id)
            message_list.append(f'From: {from_username}\nDate: {row.creation_date}\n\n{row.text}\n\n')
    for message in message_list:
        print(message + (30 * '-'))

def send_message(user_to, content):
    


if __name__ == '__main__':
    try:
        pass
    except psycopg2.OperationalError as error:
        print("Connection Error: " + error)

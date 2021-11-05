from clcrypto import hash_password
import random

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)
        
    @property
    def id(self):
        return self._id

    @property
    def password(self, password):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = password
        
    @password.setter
    def password(self, password):
        self._hashed_password = hash_password(password)
        
    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password) VALUES ('%s', '%s') RETURNING id;"""
            values = (self.username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql, values)
        return True
    
    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT * FROM Users WHERE username=%s;"
        values = (username, )
        cursor.execute(sql, values)
        data = cursor.fetchone()
        if data:
            id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None


    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        values = (id_, )
        cursor.execute(sql, values)
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users
    
    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None
        
    @property
    def id(self):
        return self._id
    
    @property
    def creation_date(self):
        return self._creation_date
    
    def save_to_db(self, cursor):
        """Saves changes to database. 
        If username eist - update informations.
        If usernema is new - create  position and return id.

        Args:
            cursor ([type]): [description]

        Returns:
            Bool: True if went good
        """        
        if self._id == -1:
            sql = """INSERT INTO Message(from_id, to_id, creation_date, text) VALUES ('%s', '%s') RETURNING id, creation_date;"""
            values = (self.from_id, self.to_id, self.text,)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
        else:
            sql = """UPDATE Message SET from_id=%s, to_id=%s, text=%s
            WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self._id)
            cursor.execute(sql, values)
        return True


    @staticmethod
    def load_all_messages(cursor):
        """Loading all messages id database

        Args:
            cursor ([type]): [description]

        Returns:
            List of objects: Each row in database is one object.
        """        
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Messages;"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages

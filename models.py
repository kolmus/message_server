import hashlib

def generate_salt():
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):

        # get a random element from the iterable
        salt += random.choice('abcdefghijklmnopqrstuvwxyz')
    return salt

def hash_password(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.

    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.

    :param str password: password to hash
    :param str salt: salt to hash, default None

    :rtype: str
    :return: hashed password
    """

    # generate salt if not provided
    if salt is None:
        salt = generate_salt()

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate haintegersh
    t_sha = hashlib.sha256()

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    # return salt & hash joined
    return salt + t_sha.hexdigest()

def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)

    :param str pass_to_check: not hashed password
    :param str hashed: hashed password

    :rtype: bool
    :return: True if password is correct, False elsewhere
    """

    # extract salt
    salt = hashed[:16]

    # extract hash to compare with
    hash_to_check = hashed[16:]

    # hash password with extracted salt
    new_hash = hash_password(pass_to_check, salt)

    # compare hashes. If equal, return True
    return new_hash[16:] == hash_to_check

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
            elf._id = cursor.fetchone()[0]
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

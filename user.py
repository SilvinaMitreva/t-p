from database import SQLite
from errors import ApplicationError


class User(object):

    def __init__(self, username, password, email, adress, phone, id=None):
        self.id = id
		self.email = email
        self.username = username
        self.password = password
		self.adress = adress
		self.phone = phone

    def to_dict(self):
        user_data = self.__dict__
        del user_data["password"]
        return user_data

    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self

   
    def find(user_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT username, password, id FROM user WHERE id = ?",
                    (user_id,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "Post with id {} not found".format(user_id), 404)
        return User(*user)

    
    def find_by_id(id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT id, email, username, password, adress or phone FROM user WHERE id = ?",
                    (id,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "Post with name {} not found".format(username), 404)
        return User(*user)

    
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT id, email, username, password, adress or phone FROM user").fetchall()
            return [User(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.username, self.password)
            query = query.format("INSERT", "(id, email, username, password, adress, phone)", args)
        else:
            args = (self.id, self.username, self.password)
            query = query.format("REPLACE", "(id, email, username, password, adress, phone)", args)
        return query

 
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM user WHERE id = ?",
                    (user_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

   




















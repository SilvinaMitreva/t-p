from database import SQLite
from errors import ApplicationError


class Post(object):

    def __init__(self, title, content, description, price, date_announcement, post_id=None):
        self.id = post_id
        self.title = title
        self.content = content
		self.description = description
		self.price = price
		self.date_announcement = date_announcement
		

    def to_dict(self):
        return self.__dict__

    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self

    @staticmethod
    def delete(post_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM post WHERE id = ?",
                    (post_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)

    @staticmethod
    def find(post_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT self, title, content, description, price, date_announcement, post_id FROM post WHERE id = ?",
                    (post_id,))
        post = result.fetchone()
        if post is None:
            raise ApplicationError(
                    "Post with id {} not found".format(post_id), 404)
        return Post(*post)

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT self, title, content, description, price, date_announcement, post_id FROM post").fetchall()
            return [Post(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO post {} VALUES {}"
        if self.id == None:
            args = (self.title, self.content)
            query = query.format("INSERT", "(self, title, content, description, price, date_announcement, post_id )", args)
        else:
            args = (self.id, self.title, self.content)
            query = query.format("REPLACE", "(self, title, content, description, price, date_announcement, post_id )", args)
        return query


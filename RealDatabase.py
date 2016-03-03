import json
from User import User
import os
import psycopg2
import urlparse

class Database():

    def __init__(self):
        x = {}
        self.items = x
        self.users = {}

        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.conn.cursor()

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        return self.items

    def addAUser(self, user):
        self.users[user.email] = user
        return user

    def getUser(self, email):
        try:
            self.cursor.execute("""select password from users where username = '{}'""".format(email))
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows[0][0]
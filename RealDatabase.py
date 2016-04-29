import json
import os
import psycopg2
import urlparse
from DatabaseUrlGenerator import getDatabaseUrl

class Database():

    def __init__(self):
        x = {}
        self.items = x
        self.users = {}

        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(getDatabaseUrl())

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.conn.cursor()

    def getQuery(self, queryString):
        try:
            self.cursor.execute(queryString)
        except:
            return ["Error"]
        rows = self.cursor.fetchall()
        return rows

    def writeQuery(self, queryString):
        try:
            self.cursor.execute(queryStatement)
        except:
            return "Error executing write query"

    def getById(self,id):
        return self.getQuery("""select * from inventory where id = '{}'""".format(id))

    def getItems(self):
        try:
            self.cursor.execute("""select * from inventory""")
        except:
            return [("exception Error")]
        rows = self.cursor.fetchall()
        return rows

    def getUser(self, username):
        try:
            self.cursor.execute("""select password from users where username = '{}'""".format(username))
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows[0][0]

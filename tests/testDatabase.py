from psycopg2.extras import Json, register_default_json
from SecretGenerator import getDatabaseUrl
from Utilities import listToCsvString
import datetime
import os
import psycopg2
import urlparse

class TestDatabase():

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = "dbname = 'travis_ci_test' host = 'localhost' user = 'postgres'"
        self.conn = psycopg2.connect(url)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        if (os.environ.get("TEST") != None):
                x = os.environ.get("TEST").split("~flask~")
                self.setUpTestDb(x)

    def getQuery(self, queryString):
        try:
            self.cursor.execute(queryString)
        except:
            print("Error executing get query")
            return ["Error"]
        rows = self.cursor.fetchall()
        return rows

    def writeQuery(self, queryString):
        # try:
        self.cursor.execute(queryString)
        # except:
            # print("Error executing write query")
            # return "Error executing write query"

    def setUpTestDb(self,y):
        from UserLoginPackage import encryptString
        register_default_json(self.conn)
        self.writeQuery("create table users (username text, password text, games text, friends text, friend_requests text, locked_out boolean default false, attempts integer default 4)")
        self.writeQuery("create table games (game_id text, game_data json, players text, turn text)")
        self.writeQuery("""insert into users (username, password) values ('test1','{}')""".format(encryptString(y[0])))
        self.writeQuery("""insert into users (username, password) values ('test2','{}')""".format(encryptString(y[1])))

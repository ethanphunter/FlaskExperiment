from SecretGenerator import getDatabaseUrl
import psycopg2
import urlparse
from models import Success, Failure

class PostgresConnection(object):

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = getDatabaseUrl()
        if (isinstance(url, str)):
            self.conn = psycopg2.connect(url)
        else:
            parsedUrl = urlparse.urlparse(url)
            self.conn = psycopg2.connect(
                database = parsedUrl.path[1:],
                user     = parsedUrl.username,
                password = parsedUrl.password,
                host     = parsedUrl.hostname,
                port     = parsedUrl.port)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def getQuery(self, queryString, parameters):
        try:
            self.cursor.execute(queryString,parameters)
        except:
            print("Error executing get query")
            return Failure("Error executing get query")
        rows = self.cursor.fetchall()
        result = Success(rows)
        return result

    def writeQuery(self, queryString, parameters):
        try:
            self.cursor.execute(queryString, parameters)
            return Success("Write Query Successful")
        except:
            print("Error executing write query")
            return Failure("Error executing write query")

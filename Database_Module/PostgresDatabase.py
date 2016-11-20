from PostgresConnection import PostgresConnection

class PostgresDatabase(PostgresConnection):
    """
    Description: A query layer for the postgres database.
    Note: All of these functions should return a Success or a Failure object.
    """
    def __init__(self):
        super(PostgresDatabase,self).__init__()

    """
        These queries are for user interactions.
        This includes checking passwords, and checking if the user is locked out.
    """

    def getUser(self, username):
        """Deprecated: use `getUsersPassword`"""
        try:
            self.cursor.execute("""select password from users where username = '{}'""".format(username))
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows[0][0]

    def getUsersPassword(self,username):
        return self.getQuery("""select password from users where username = (%s)""", (username,))

    def getUser2(self):
        return self.getQuery("""select username from users where username = (%s)""", ("dev",))

    def userExists(self,username):
        return self.getQuery("""select count(username) from users where username = (%s)""", (username, ))

    def changePassword(self,username,password):
        return self.writeQuery("""update users set password = (%s) where username = (%s)""", (password, username))

    def userIsLockedOut(self,username):
        return self.getQuery("""select locked_out from users where username = (%s)""", (username,))

    def lockOutUser(self,username):
        return self.writeQuery("""update users set locked_out = true where username = (%s)""", (username, ))

    def getNumberOfAttempts(self,username):
        return self.getQuery("""select attempts from users where username = (%s)""", (username, ))

    def updateNumberOfAttempts(self,username,number):
        return self.writeQuery("""update users set attempts = (%s) where username = (%s)""", (number, username))

    """
        These queries are used for friend interactions.
        This includes accepting/declining friend requests, and removing friends
    """
    def getAllUsernames(self):
        return self.getQuery("""select username from users""")

    def getFriendsForUser(self, username):
        return self.getQuery("""select friends from users where username = (%s)""", (username, ))

    def getFriendRequestsForUser(self, username):
        return self.getQuery("""select friend_requests from users where username = (%s)""", (username, ))

    def updateFriendList(self, username, newFriendList):
        return self.writeQuery("""update users set friends = (%s) where username = (%s)""", (newFriendList, username))

    def updateFriendRequestList(self, username, newFriendRequestList):
        return self.writeQuery("""update users set friend_requests = (%s) where username = (%s)""", (newFriendRequestList, username))

    """
        These queries are for handling interactions with games.
        This includes adding/removing games, and updating them.
    """

    def gameIdExists(self,gameId):
        return self.getQuery("""select count(game_id) from games where game_id = (%s)""", (gameId, ))

    def getGameIdsForUser(self,username):
        return self.getQuery("""select games from users where username = (%s)""", (username, ))

    def updateGameIdsForUser(self,newGameIds,username):
        return self.writeQuery("""update users set games = (%s) where username = (%s)""", (newGameIds, username))

    def getByGameId(self,gameId):
        return self.getQuery("""select * from games where game_id = (%s)""", (gameId, ))

    def getGameDataById(self,gameId):
        return self.getQuery("""select game_data from games where game_id = (%s)""", (gameId, ))

    def getGameDetails(self,gameId):
        return self.getQuery("""select game_id, players, turn from games where game_id = (%s)""", (gameId, ))

    def getAllGameIds(self):
        return self.getQuery("""select game_id from games""", ())

    def getMaxGameId(self):
        return self.getQuery("""select max(game_id) from games""", ())

    def createGame(self,gameId,gameData,players,turn):
        return self.writeQuery("""insert into games values ((%s), (%s), (%s),(%s))""", (gameId, Json(gameData), players, turn))

    def updateGame(self,gameId,gameData,turn):
        self.writeQuery("""update games set game_data = (%s), turn = (%s) where game_id = (%s)""", (Json(gameData), turn, gameId))

    def deleteGameByGameId(self,gameId):
        self.writeQuery("""delete from games where game_id = (%s)""", (gameId, ))

    """
        These are extra queries that don't fit in the other sections.
    """

    def enterLogMessage(self,message):
        dt = datetime.datetime.now()
        queryString = """insert into logs (message, time) values ((%s), (%s))"""
        return self.writeQuery(queryString, (message, psycopg2.Timestamp(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)))

    def getById(self,id):
        return self.getQuery("""select * from inventory where id = (%s)""", (id,))

    def getItems(self):
        return self.getQuery("""select * from inventory""", ())

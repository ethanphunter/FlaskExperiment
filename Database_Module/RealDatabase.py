from psycopg2.extras import Json, register_default_json
from SecretGenerator import getDatabaseUrl
from Utilities import listToCsvString
import datetime
import os
import psycopg2
import urlparse

class Database():

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

    def getQuery(self, queryString):
        try:
            self.cursor.execute(queryString)
        except:
            print("Error executing get query")
            return ["Error"]
        rows = self.cursor.fetchall()
        return rows

    def writeQuery(self, queryString):
        try:
            self.cursor.execute(queryString)
            return "Success"
        except:
            print("Error executing write query")
            return "Error executing write query"

    def setUpTestDb(self,y):
        from UserLoginPackage import encryptString
        register_default_json(self.conn)
        self.writeQuery("create table users (username text, password text, games text, friends text, friend_requests text, locked_out boolean default false, attempts integer default 4)")
        self.writeQuery("create table games (game_id text, game_data json, players text, turn text)")
        print(self.getQuery("select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = 'games'"))
        self.writeQuery("""insert into users (username, password) values ('test1','{}')""".format(encryptString(y[0])))
        self.writeQuery("""insert into users (username, password) values ('test2','{}')""".format(encryptString(y[1])))

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

    def changePassword(self,username,password):
        return self.writeQuery("""update users set password = '{password}' where username = '{username}'""".format(password = password, username = username))

    def userIsLockedOut(self,username):
        return self.getQuery("""select locked_out from users where username = '{username}'""".format(username=username))

    def lockOutUser(self,username):
        return self.writeQuery("""update users set locked_out = true where username = '{username}'""".format(username = username))

    def getNumberOfAttempts(self,username):
        return self.getQuery("""select attempts from users where username = '{username}'""".format(username = username))

    def updateNumberOfAttempts(self,username,number):
        return self.writeQuery("""update users set attempts = {number} where username = '{username}'""".format(username = username, number = number))

    def getAllUsernames(self):
        return self.getQuery("""select username from users""")

    def getFriendsForUser(self, username):
        return self.getQuery("""select friends from users where username = '{username}'""".format(username = username))

    def getFriendRequestsForUser(self, username):
        return self.getQuery("""select friend_requests from users where username = '{username}'""".format(username = username))

    def acceptFriendRequest(self, username, otherUsername):
        oldFriendList = self.getFriendsForUser(username)
        if (oldFriendList == [(None,)] or oldFriendList == [("",)]):
            newFriendList = otherUsername
        else:
            newFriendList = oldFriendList[0][0] + "," + otherUsername
        return self.writeQuery("""update users set friends = '{friendList}' where username = '{username}'""".format(friendList = newFriendList, username = username))

    def removeFriendRequest(self, username, otherUsername):
        oldFriendRequests = self.getFriendRequestsForUser(username)
        if (oldFriendRequests == [(None,)]):
            newFriendRequestList = ""
        else:
            csv = oldFriendRequests[0][0].split(",")
            csv.remove(otherUsername)
            newFriendRequestList = listToCsvString(csv)
        return self.writeQuery("""update users set friend_requests = '{friend_requests}'""".format(friend_requests = newFriendRequestList))

    def removeFriend(self,username,friend):
        oldFriendsCsv = self.getFriendsForUser(username)
        if (oldFriendsCsv == [(None,)] or oldFriendsCsv == [("",)]):
            oldFriends = []
        else:
            oldFriends = oldFriendsCsv[0][0].split(",")
        if (friend in oldFriends):
            oldFriends.remove(friend)
        else:
            print("~" + username + "~ is not friends with ~" + friend + "~")
            return None
        newFriends = listToCsvString(oldFriends)
        return self.writeQuery("""update users set friends = '{friends}' where username = '{username}'""".format(friends = newFriends, username = username))

    def addFriend(self,username,otherUsername):
        oldFriendRequests = self.getFriendRequestsForUser(username)
        if (oldFriendRequests == [(None,)] or oldFriendRequests == [] or oldFriendRequests == [("",)]):
            newFriendRequestList = otherUsername
        else:
            newFriendRequestList = oldFriendRequests[0][0] + "," + otherUsername
        return self.writeQuery("""update users set friend_requests = '{friend_requests}' where username = '{username}'""".format(friend_requests = newFriendRequestList, username = username))

    def getGamesForUser(self,userName):
        return self.getQuery("""select games from users where username = '{}'""".format(userName))

    def getByGameId(self,gameId):
        return self.getQuery("""select * from games where game_id = '{game_id}'""".format(game_id=gameId))

    def getAllGameIds(self):
        return self.getQuery("""select game_id from games""")

    def getMaxGameId(self):
        return self.getQuery("""select max(game_id) from games""")

    def createGame(self,gameId,gameData,players,turn):
        return self.writeQuery("""insert into games values ('{game_id}', {game_data}, '{players}','{turn}')""".format(game_id = gameId, game_data = Json(gameData), players=players, turn=turn))

    def updateGame(self,gameId,gameData,turn):
        self.writeQuery("""update games set game_data = {gameData}, turn = '{turn}' where game_id = '{gameId}'""".format(gameData = Json(gameData), turn = turn, gameId = gameId))

    def deleteGameByGameId(self,gameId):
        self.writeQuery("""delete from games where game_id = '{gameId}'""".format(gameId=gameId))

    def addGameIdToUser(self,gameId,userName):
        gameIds = self.getGamesForUser(userName)
        print(gameIds)
        if (gameIds == [(None,)] or gameIds == [("",)]):
            print("No games for " + userName)
            print("Adding game Id " + gameId + " to " + userName)
            newGameIds = gameId
        else:
            newGameIds = gameIds[0][0] + "," + gameId
        return self.writeQuery("""update users set games = '{gameIds}' where username = '{userName}'""".format(gameIds = newGameIds, userName = userName))

    def deleteGameIdForUser(self,gameId,userName):
        gameIds = self.getGamesForUser(userName)
        if (gameIds != [(None,)]):
            gameIdList = gameIds[0][0].split(",")
            newGameIdsCsv = ""
            for gId in gameIdList:
                if (gId != gameId):
                    if (newGameIdsCsv == ""):
                        newGameIdsCsv += gId
                    else:
                        newGameIdsCsv += "," + gId
            return self.writeQuery("""update users set games = '{gameIds}' where username = '{userName}'""".format(gameIds = newGameIdsCsv, userName = userName))

        else:
            return "Error: No Game Ids for user"

    def enterLogMessage(self,message):
        dt = datetime.datetime.now()
        queryString = """insert into logs (message, time) values ('{message}', {time});""".format(message = message, time = psycopg2.Timestamp(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second))
        return self.writeQuery(queryString)

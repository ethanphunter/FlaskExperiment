from Utilities import *
from Games_Module.ChessGame_Module.ChessGame import ChessGame
from Games_Module.GameJson import GameJSONDecoder

class DataBaseUtils(object):
    def __init__(self,db):
        self.db = db
        self.jsonDecoder = GameJSONDecoder()

    def getGamesForUser(self,userName):
        """Returns a list of games for a user"""
        gameIdsCsv = self.db.getGamesForUser(userName)
        if (gameIdsCsv == [(None,)] or gameIdsCsv == [] or gameIdsCsv == [("",)]):
            return []
        else:
            gameIds = intifyList(gameIdsCsv[0][0].split(","))
            games = []
            for game_id in gameIds:
                game = self.db.getByGameId(game_id)[0]
                game_data = game[1]
                players = game[2]
                if ("chessGame" in game_data):
                    theGame = ChessGame(str(game_id),players)
                    theGame.decode(game_data.get("chessGame"))
                    games.append(theGame)
            return games

    def createGame(self,gameName,players):
        if (gameName == "ChessGame"):
            game = ChessGame(str(self.getNextGameId()),players)
            self.db.createGame(game.getId(),game.json(),players[0] + "," + players[1],game.getWhoseTurn())
            for player in players:
                self.db.addGameIdToUser(game.getId(),player)
            return game
        else:
            print("Error, game: " + gameName + " Does not exist")
            return None

    def updateGame(self,game):
        print("UpdateGame says it's " + game.getWhoseTurn() + "'s turn")
        # self.db.deleteGameByGameId(game.getId())
        self.db.updateGame(game.getId(),game.json(),game.getWhoseTurn())

    def deleteGame(self,gameId,user):
        print("User: '" + user + "', is deleting a game with gameId: " + gameId)
        game = self.getGame(gameId)
        players = game.getPlayers()
        if (user in players):
            gameId = game.getId()
            a = self.db.deleteGameIdForUser(gameId,players[0])
            b = self.db.deleteGameIdForUser(gameId,players[1])
            c = self.db.deleteGameByGameId(gameId)
            if (a == None and b == None and c == None):
                return ""
            else:
                return "Query Error"
        else:
            "Error Game Not Deleted"


    def getGame(self,gameId):
        gameRow = self.db.getByGameId(gameId)[0]
        gameData = gameRow[1]
        players = gameRow[2]
        turn = gameRow[3]
        game = self.jsonDecoder.decode(gameData)
        return game


    def getNextGameId(self):
        gameId = self.db.getMaxGameId()[0][0]
        return int(gameId) + 1
        # print(self.db.getMaxGameId())
        # highest = 0
        # for gameId in gameIds:
        #     intedGameId = int(gameId[0])
        #     if (intedGameId > highest):
        #         highest = intedGameId
        # return highest + 1

    def getFriends(self,username):
        csv = self.db.getFriendsForUser(username)
        if (csv == [(None,)] or csv == []):
            return []
        else:
            return csv[0][0].split(",")

    def getFriendRequests(self,username):
        requests = self.db.getFriendRequestsForUser(username)
        if (requests == [(None,)] or requests == [] or requests == [("",)]):
            return []
        else:
            return requests[0][0].split(",")

    def acceptFriendRequest(self,username,otherUsername):
        x = self.db.acceptFriendRequest(username,otherUsername)
        y = self.db.acceptFriendRequest(otherUsername,username)
        a = self.db.removeFriendRequest(username,otherUsername)
        # b = self.db.removeFriendRequest(otherUsername,username)
        return toFlaskDelimitedString([x,a])

    def declineFriendRequest(self,username,otherUsername):
        # x = self.db.removeFriendRequest(username,otherUsername)
        y = self.db.removeFriendRequest(otherUsername,username)
        return y

    def addFriendRequest(self,username,otherUsername):
        currentFriendsCsv = self.db.getFriendsForUser(username)
        users = self.db.getAllUsernames()
        flag = False
        for u in users:
            if (otherUsername == u[0]):
                flag = True
        if (not flag):
            return "Error, user: '" + otherUsername + "' does not exist"
        if (currentFriendsCsv == [(None,)]):
            currentFriends = []
        else:
            currentFriends = currentFriendsCsv[0][0].split(",")
        if (otherUsername in currentFriends):
            return "Error, already friends"
        else:
            # x = self.db.addFriend(username,otherUsername)
            x = self.db.getFriendRequestsForUser(username)
            if (not (x == [(None,)] or x == [] or x == [("",)])):
                requests = x[0][0].split(",")
                if (otherUsername in requests):
                    return "Error, Request Already Sent"
            else:
                a = self.db.addFriend(otherUsername,username)
                return "Request sent"

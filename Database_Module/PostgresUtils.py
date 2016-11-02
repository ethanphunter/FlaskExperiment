from Utilities import *
from models import Success, Failure
from Games_Module.ChessGame_Module.ChessGame import ChessGame
from Games_Module.GameJson import GameJSONDecoder
from Games_Module.GamesModels import GameDetails
from UserLoginPackage import changePassword
from PostgresDatabase import PostgresDatabase

class PostgresUtils(object):
    def __init__(self):
        self.database = PostgresDatabase()

    def getGameDetailsForUser(self,userName):
        """
            Input: userName: String
            Output: List[GameDetails]
            Description: Returns a list of GameDetails for the given userName.
                Returns an empty list if the username does not exist.
        """
       gameIdsData = self.database.getGameIdsForUser(userName).getOrElse([])
       games = []
        if (gameIdsData == [] or gameIdsData == [("", )]):
            games = []
        else:
            gameIds = intifyList(gameIdsData[0][0].split(","))
            for gameId in gameIds:
                details = self.database.getGameDetails(gameId)
                if (details.isSuccess()):
                    d = details.get()
                    gd = GameDetails(d[0][0],d[0][1],d[0][2])
                    games.append(gd)
                else:
                    print("Error getting details for game {}".format(gameId))
        return games

    def getGameFromGameId(self,gameId):
        """
            Input: gameId: String
            Output: Success[Game] or Failure
        """
        if (self.database.gameIdExists(gameId).getOrElse([(0,)])[0][0] != 1):
            return Failure("Game Id doesn't exist")
        else:
            gameRowResult = self.database.getByGameId(gameId)
            if (gameRowResult.isFailure()):
                return Failure("Failed to get game from the database")
            else:
                gameData = gameRowResult.get()[0][0]
                decodedGame = self.jsonDecoder.decode(gameData)
                return Success(decodedGame)

    def createGame(self,gameName,players):
        """
            Input: gameName: String, players: List[String]
            Output: Success[Game] or Failure
        """
        gameId = self.getNextGameId()
        if (not self.playersExist(players)):
            return Failure("User does not exist")
        elif (gameName == "ChessGame"):
            game = ChessGame(str(gameId),players)
            playerOneIds = self.database.getGameIdsForUser(players[0]).get()[0][0]
            newPlayerOneIds = listToCsvString(playerOneIds.split(",").append(gameId))

            playerTwoIds = self.database.getGameIdsForUser(players[1]).get()[0][0]
            newPlayerTwoIds = listToCsvString(playerTwoIds.split(",").append(gameId))

            updateOne = self.database.updateGameIdsForUser(newPlayerOneIds,players[0])
            updateTwo = self.database.updateGameIdsForUser(newPlayerTwoIds,players[1])
            if (updateOne.isSuccess() and updateTwo.isSuccess()):
                return Success(game)
            else:
                Failure("Failed to update game ids for a user")
        else:
            return Failure("Generic Failure")

    def playersExist(self,players):
        """
            Input: players: List[String]
            Output: Boolean
            Description: Checks to see if a list of players exist.
        """
        allPlayersExist = True
        for player in players:
            exists = self.database.userExists(player).getOrElse([(False,)])[0][0]
            if (not exists):
                allPlayersExist = False
        return allPlayersExist

    def updateGame(self,game):
        """
            Input: game: Game
            Output: Success[String] or Failure
        """
        return self.database.updateGame(game.getId(), game.json(), game.getWhoseTurn())

    def deleteGame(self,gameId,user):
        """
            Input: gameId: String, user: String
            Output: Success[String] or Failure
            Description: Deletes a game given a gameId and the user deleting the game.
        """
        print("User: '" + user + "', is deleting a game with gameId: " + gameId)
        maybeGame = self.getGameFromGameId(gameId)
        if (maybeGame.isFailure()):
            return maybeGame
        else:
            game = maybeGame.get()
            players = game.getPlayers()
            if (user not in players):
                return Failure("User is not a part of this game")
            else:
                maybeDeltedGameA = self.deleteGameIdForUser(gameId,players[0])
                maybeDeltedGameB = self.deleteGameIdForUser(gameId,players[0])
                maybeDeletedGameData = self.database.deleteGameByGameId(gameId)
                if (maybeDeltedGameA.isFailure()):
                    return maybeDeltedGameA
                elif (maybeDeltedGameB.isFailure()):
                    return maybeDeltedGameB
                elif (maybeDeletedGameData.isFailure()):
                    return Failure("Failed to delete game data ~" +
                        maybeDeletedGameData.getErrorMessage())

    def deleteGameIdForUser(self,gameId,username):
        """
            Input: gameId: String, username: String
            Output: Success[String] or Failure
        """
        if (self.database.userExists(username).getOrElse([(0,)])[0][0] != 1):
            return Failure("User does not exist!")
        else:
            maybeGameIds = self.database.getGameIdsForUser(username)
            gameIds = maybeGameIds.getOrElse([("",)])[0][0].split(",")
            if (gameId not in gameIds):
                return Failure("GameId does not exist for user")
            else:
                gameIds.remove(gameId)
                newGameIdsCsv = listToCsvString(gameIds)
                return self.database.updateGameIdsForUser(newGameIdsCsv,username)

    def getNextGameId(self):
        """
            Input:
            Output: Success[Int] or Failure
        """
        maybeMaxGameId = self.database.getMaxGameId()
        if (maybeMaxGameId.isFailure()):
            return maybeMaxGameId
        else:
            maxGameId = maybeMaxGameId.get()
            if (maxGameId == []):
                return Success(1)
            else:
                return Success(maxGameId + 1)

from Utilities import *
from models import Success, Failure
from Games_Module.ChessGame_Module.ChessGame import ChessGame
from Games_Module.GameJson import GameJSONDecoder
from Games_Module.GamesModels import GameDetails
from UserLoginPackage import changePassword
from PostgresDatabase import PostgresDatabase
from passlib.apps import custom_app_context as encryption_context

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

    def getFriendsForUser(self,username):
        """
            Input: username: String
            Output: Success[List[String]] or Failure
        """
        if (self.database.userExists(username).getOrElse(0) != 1):
            return Failure("User does not exist!")
        else:
            maybeFriendCsv = self.database.getFriendsForUser(username)
            if (maybeFriendCsv.isFailure()):
                return maybeFriendCsv
            else:
                friendsCsv = maybeFriendCsv.get()[0][0]
                return friendsCsv.split(",")

    def getFriendRequestsForUser(self,username):
        """
            Input: username: String
            Output: Success[List[String]] or Failure
        """
        if (self.database.userExists(username).getOrElse(0) != 1):
            return Failure("User does not exist!")
        else:
            maybeFriendRequestsCsv = self.database.getFriendRequestsForUser(username)
            if (maybeFriendRequestsCsv.isFailure()):
                return maybeFriendRequestsCsv
            else:
                friendRequestsCsv = maybeFriendRequestsCsv.get()[0][0]
                return friendRequestsCsv.split(",")

    def acceptFriendRequest(self,username,otherUsername):
        """
            Input: username: String, otherUsername: String
            Output: Success[String] or Failure
        """
        isRealPlayers = self.playersExist([username,otherUsername])
        if (isRealPlayers):
            return Failure("User does not exist!")
        else:
            userOneRequests = self.getFriendRequestsForUser(username)
            userOneFriends  = self.getFriendsForUser(username)
            userTwoFriends  = self.getFriendsForUser(otherUsername)
            if (userOneRequests.isFailure()):
                return userOneRequests
            elif (userOneFriends.isFailure()):
                return userOneFriends
            elif (userTwoFriends.isFailure()):
                return userTwoFriends
            else:
                newUserOneRequests = userOneRequests.getOrElse([])
                newUserOneFriends  = userOneFriends.getOrElse([])
                newUserTwoFriends  = userTwoFriends.getOrElse([])
                if (otherUsername not in newUserOneRequests):
                    return Failure("Other user is not in users requests")
                elif (otherUsername in newUserOneFriends or username in newUserTwoFriends):
                    return Failure("Users are already friends")
                else:
                    newUserOneRequests.remove(otherUsername)
                    newUserOneFriends.append(otherUsername)
                    newUserTwoFriends.append(username)
                    resultOne   = self.database.updateFriendRequestList(username,listToCsvString(newUserOneRequests))
                    resultTwo   = self.database.updateFriendList(username,listToCsvString(newUserOneFriends))
                    resultThree = self.database.updateFriendList(otherUsername,listToCsvString(newUserTwoFriends))
                    if (resultOne.isFailure()):
                        return resultOne
                    elif (resultTwo.isFailure()):
                        return resultTwo
                    elif (resultThree.isFailure()):
                        return resultThree
                    else:
                        return Success("Friend Request Accepted")

    def declineFriendRequest(self,username,otherUsername):
        """
            Input: username: String, otherUsername: String
            Output: Success[String] or Failure
        """
        userRequests = self.getFriendRequestsForUser(username)
        if (userRequests.isFailure()):
            return userRequests
        else:
            newUserRequests = userRequests.getOrElse([])
            if (otherUsername not in newUserRequests):
                return Failure("Other user not in users friend requests")
            else:
                newUserRequests.remove(otherUsername)
                result = self.database.updateFriendRequestList(username,listToCsvString(newUserRequests))
                return result

    def addFriendRequest(self,username,otherUsername):
        """
            Input: username: String, otherUsername: String
            Output: Success[String] or Failure
            Description: username should be the current user and otherUsername
                should be the user they are requesting to be friends with.
        """
        isRealPlayers = self.playersExist([username,otherUsername])
        if (not isRealPlayers):
            return Failure("User does not exist!")
        else:
            userOnerequests = self.getFriendRequestsForUser(username)
            userTwoRequests = self.getFriendRequestsForUser(otherUsername)
            if (userOnerequests.isFailure()):
                return userOnerequests
            elif (userTwoRequests.isFailure()):
                return userTwoRequests
            else:
                userOneRequestsList = csvToList(userOnerequests.getOrElse(""))
                userTwoRequestsList = csvToList(userTwoRequests.getOrElse(""))
                if (username in userTwoRequestsList):
                    return Failure("User has already made this request")
                elif (otherUsername in new userOneRequestsList):
                    return Failure("The other user has already sent this user a request")
                else:
                    userOneRequestsList.append(otherUsername)
                    result = self.database.updateFriendRequestList(username,listToCsvString(userOneRequestsList))
                    return result

    def removeFriend(self,username,friend):
        """
            Input: username: String, friend: String
            Output: Success[String] or Failure
        """
        isRealPlayers = self.playersExist([username,friend])
        if (not isRealPlayers):
            return Failure("User does not exist!")
        else:
            userOneFriends = self.getFriendsForUser(username)
            userTwoFriends  = self.getFriendsForUser(friend)
            if (userOneFriends.isFailure()):
                return userOneFriends
            if (userTwoFriends.isFailure()):
                return userTwoFriendsCsv
            else:
                userOneFriendsList = csvToList(userOneFriends.getOrElse([]))
                userTwoFriendsList = csvToList(userTwoFriends.getOrElse([]))
                if (friend not in userOneFriendsList):
                    return Failure("User is not friends with this other user")
                elif (username not in userTwoFriendsList):
                    return Failure("Friend is not friends with this user")
                else:
                    userOneFriendsList.remove(friend)
                    userTwoFriendsList.remove(username)
                    resultOne = self.database.updateFriendList(username,listToCsvString(userOneFriendsList))
                    resultTwo = self.database.updateFriendList(friend,listToCsvString(userTwoFriendsList))
                    if (resultOne.isFailure()):
                        return resultOne
                    elif (resultTwo.isFailure()):
                        return resultTwo
                    else:
                        return Success("Friend Removed")

    def changeUsersPassword(self,username,oldPassword,newPassword):
        playerExists = self.database.userExists(username)
        if (playerExists.getOrElse(0) != 1):
            return Failure("User does not exist!")
        else:
            if (username == "uni"):
                return Failure("Cannot update password")
            else:
                maybePasswordHash = self.database.getUsersPassword(username)
                if (maybePasswordHash.isFailure()):
                    return Failure("Failed to get users old password")
                else:
                    if (encryption_context.verify(oldPassword,maybePasswordHash.getOrElse(""))):
                        result = self.database.changePassword(username,self.encryptString(newPassword))
                        if (result.isFailure()):
                            logResultOne = self.database.enterLogMessage("Update password Query error for user: '" + username + "'")
                            if (logResultOne.isFailure()):
                                print(logResultOne.getErrorMessage())
                            return result
                        else:
                            logResultTwo = self.database.enterLogMessage("'" + username + "' changed their password")
                            if (logResultTwo.isFailure()):
                                print(logResultTwo.getErrorMessage())
                            return Success("Password Changed Successfully")

    #Private
    def encryptString(string):
        return encryption_context.encrypt(string)

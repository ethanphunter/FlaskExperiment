from flask import Blueprint, render_template, session, request, redirect
from UserLoginPackage import requireLogin

def GamesBluePrintConstructor(dataBaseUtils):
    dbutils = dataBaseUtils

    GamesBluePrint = Blueprint("Games",__name__,template_folder="templates")

    @GamesBluePrint.route("/userSettings")
    def userSettings():
        requireLogin()
        username = session.get("current_user")
        return render_template("Settings.html",userName = username)

    @GamesBluePrint.route("/changePassword", methods=["POST"])
    def changePasswordEndpoint():
        requireLogin()
        return changePassword(db)

    @GamesBluePrint.route("/addFriend", methods=["POST"])
    def addFriend():
        requireLogin()
        username = session.get("current_user")
        otherUsername = request.form["friend_username"]
        error = dbutils.addFriendRequest(username,otherUsername)
        session["friend_error"] = error
        return redirect("/gameList")

    @GamesBluePrint.route("/acceptFriendRequest", methods=["POST"])
    def acceptFriendRequest():
        requireLogin()
        username = session.get("current_user")
        friendUsername = request.form["friend_username"]
        dbutils.acceptFriendRequest(username,friendUsername)
        return redirect("/gameList")

    @GamesBluePrint.route("/declineFriendRequest", methods=["POST"])
    def declineFriendRequest():
        requireLogin()
        username = session.get("current_user")
        otherUsername = request.form["friend_username"]
        dbutils.declineFriendRequest(username,otherUsername)
        return redirect("/gameList")

    @GamesBluePrint.route("/startGame", methods=["POST"])
    def startGame():
        requireLogin()
        otherUsername = request.form["user"]
        if (otherUsername == ""):
            return redirect("/gameList")
        username = session.get("current_user")
        game = dbutils.createGame("ChessGame",[username,otherUsername])
        session["chessGame"] = game
        return redirect("/board")

    @GamesBluePrint.route("/gameList")
    def gameList():
        requireLogin()
        session["gameId"] = ""
        session["BoardError"] = ""
        username = session.get("current_user")
        games = dbutils.getGamesForUser(username)
        return render_template("GameList.html",
                    games = games,
                    userName = username,
                    friendError = session.get("friend_error"),
                    friendRequests = dbutils.getFriendRequests(username),
                    friends = dbutils.getFriends(username))

    @GamesBluePrint.route("/closeFriendError")
    def closeFriendError():
        session["friend_error"] = ""
        return redirect("/gameList")

    @GamesBluePrint.route("/deleteGame", methods=["POST"])
    def deleteGame():
        gameId = request.form["gameId"]
        print(dbutils.deleteGame(gameId,session.get("current_user")))
        return redirect("/gameList")

    @GamesBluePrint.route("/openGame", methods=["POST"])
    def openGame():
        gameId = request.form["gameId"]
        if (gameId == ""):
            return redirect("/gameList")
        else:
            game = dbutils.getGame(gameId)
            session["chessGame"] = game
            session["gameId"] = gameId
            return redirect("/board")

    return GamesBluePrint

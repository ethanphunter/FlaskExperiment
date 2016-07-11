"""
Author: Ethan Hunter
Comments: A simple Flask app for me to mess around with.
"""

from flask import Flask, render_template, request, redirect, session
from RealDatabase import Database
from databaseUtils import DataBaseUtils
from UserLoginPackage import login, logout, requireLogin, loginWithRealDb, changePassword
from chessGame import *
from GameJson import *
from SecretGenerator import getSecretKey

# db = MyDatabase()
db = Database()
dbutils = DataBaseUtils(db)
gameJsonDecoder = GameJSONDecoder()
app = Flask(__name__)

# Set Debug to true for development purposes
# SECRET_KEY is used in the session object
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = getSecretKey()))

app.json_encoder = GameJSONEncoder
# app.json_decoder = GameJSONDecoder

# This is how you define a route
@app.route("/")
def index():
    session["BoardError"] = ""
    #The return statement determines what html the user sees
    return render_template("index.html")

# In the html there is a form element that posts to this endpoint
# This route just prints the email that was submitted in the email input field
@app.route("/form", methods=["POST"])
def form():
    email = request.form["email"]
    print(email)
    return redirect("/")

@app.route("/search", methods=["POST"])
def search():
    results = db.getById(str(request.form["id"]))
    print(results)
    return render_template("searchResults.html", results = results)

# Log a user in. This is a pretty simple way of doing it, but it works
@app.route("/login", methods=["GET","POST"])
def signIn():
    return loginWithRealDb(db) #defined in the user login package

# Log the user out
@app.route("/logout")
def signOut():
    return logout() #defined in the user login package

# You should only be able to access this if you are logged in
@app.route("/secret")
def secret():
    requireLogin()
    return "Current User: " + session.get("current_user")

@app.route("/userSettings")
def userSettings():
    requireLogin()
    username = session.get("current_user")
    return render_template("settings.html",userName = username)

@app.route("/changePassword", methods=["POST"])
def changePasswordEndpoint():
    requireLogin()
    return changePassword(db)

@app.route("/addFriend", methods=["POST"])
def addFriend():
    requireLogin()
    username = session.get("current_user")
    otherUsername = request.form["friend_username"]
    error = dbutils.addFriendRequest(username,otherUsername)
    session["friend_error"] = error
    return redirect("/gameList")

@app.route("/acceptFriendRequest", methods=["POST"])
def acceptFriendRequest():
    requireLogin()
    username = session.get("current_user")
    friendUsername = request.form["friend_username"]
    dbutils.acceptFriendRequest(username,friendUsername)
    return redirect("/gameList")

@app.route("/declineFriendRequest", methods=["POST"])
def declineFriendRequest():
    requireLogin()
    username = session.get("current_user")
    otherUsername = request.form["friend_username"]
    dbutils.declineFriendRequest(username,otherUsername)
    return redirect("/gameList")

@app.route("/startGame", methods=["POST"])
def startGame():
    requireLogin()
    otherUsername = request.form["user"]
    if (otherUsername == ""):
        return redirect("/gameList")
    username = session.get("current_user")
    game = dbutils.createGame("ChessGame",[username,otherUsername])
    session["chessGame"] = game
    return redirect("/board")

@app.route("/board")
def board():
    requireLogin()
    game = gameJsonDecoder.decode(session.get("chessGame"))
    return render_template("board.html", game = game, error = session.get("BoardError"), userName = session.get("current_user"))

@app.route("/closeError")
def closeError():
    session["BoardError"] = ""
    return redirect("/board")

@app.route("/makeMove", methods=["POST"])
def makeMove():
    session["BoardError"] = ""
    fromRow = int(request.form["from-row"]) - 1
    fromCol = request.form["from-col"]
    toRow = int(request.form["to-row"]) - 1
    toCol = request.form["to-col"]
    game = gameJsonDecoder.decode(session.get("chessGame"))
    if (game.isPlayersTurn(session.get("current_user"))):
        error = game.makeMove(fromRow,fromCol,toRow,toCol)
        if (error != ""):
            session["BoardError"] = error
            print("There was a board error")
        else:
            session["chessGame"] = game
            print("Updating game in the db...")
            dbutils.updateGame(game)
            print("Game updated")
    else:
        session["BoardError"] = "Not Your Turn!"
    return redirect("/board")

@app.route("/gameList")
def gameList():
    requireLogin()
    session["BoardError"] = ""
    username = session.get("current_user")
    games = dbutils.getGamesForUser(username)
    return render_template("GameList.html",
                games = games,
                userName = username,
                friendError = session.get("friend_error"),
                friendRequests = dbutils.getFriendRequests(username),
                friends = dbutils.getFriends(username))

@app.route("/closeFriendError")
def closeFriendError():
    session["friend_error"] = ""
    return redirect("/gameList")

@app.route("/deleteGame", methods=["POST"])
def deleteGame():
    gameId = request.form["gameId"]
    print(dbutils.deleteGame(gameId,session.get("current_user")))
    return redirect("/gameList")

@app.route("/openGame", methods=["POST"])
def openGame():
    gameId = request.form["gameId"]
    if (gameId == ""):
        return redirect("/gameList")
    else:
        game = dbutils.getGame(gameId)
        session["chessGame"] = game
        return redirect("/board")

if (__name__ == "__main__"):
    app.run()

"""
Author: Ethan Hunter
Comments: A simple Flask app for me to mess around with.
"""

import Database_Module
import Games_Module
import Games_Module.ChessGame_Module

from Games_Module.GamesBluePrint import GamesBluePrintConstructor
from Games_Module.ChessGame_Module.ChessGameBluePrint import ChessGameBluePrintConstructor
from Database_Module.RealDatabase import Database
from Database_Module.DatabaseUtils import DataBaseUtils
from Database_Module.PostgresDatabase import PostgresDatabase
from Games_Module.GameJson import *

from flask import Flask, render_template, request, redirect, session
from UserLoginPackage import logout, requireLogin, loginWithRealDb, changePassword
from SecretGenerator import getSecretKey

db = Database()
dbutils = DataBaseUtils(db)
gameJsonDecoder = GameJSONDecoder()
app = Flask(__name__)
app.register_blueprint(GamesBluePrintConstructor(dbutils))
app.register_blueprint(ChessGameBluePrintConstructor(dbutils,gameJsonDecoder))

# Set Debug to true for development purposes
# SECRET_KEY is used in the session object
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = getSecretKey()))

app.json_encoder = GameJSONEncoder
database = PostgresDatabase()

@app.route("/test")
def test():
    return str(database.getUser2().getOrElse("Failure"))

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

if (__name__ == "__main__"):
    # app.run(host='0.0.0.0') #For running on a local network
    app.run()

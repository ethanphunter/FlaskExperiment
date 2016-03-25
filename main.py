"""
Author: Ethan Hunter
Comments: A simple Flask app for me to mess around with.
"""

from flask import Flask, render_template, request, redirect, session, abort, jsonify
from Database import MyDatabase
from RealDatabase import Database
from UserLoginPackage import login, logout, requireLogin, loginWithRealDb

db = MyDatabase()
# otherdb = Database()
app = Flask(__name__)

# Set Debug to true for development purposes
# SECRET_KEY is used in the session object
app.config.update(dict(
    #DEBUG=True,
    SECRET_KEY='A Very Very Secret Key'))

# This is how you define a route
@app.route("/")
def index():
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
    results = [db.getById(str(request.form["id"]))]
    return render_template("searchResults.html", results = results)

@app.route("/inventory")
def inventory():
    return render_template("inventory.html", items = db.getItems())

# Log a user in. This is a pretty simple way of doing it, but it works
@app.route("/login", methods=["GET","POST"])
def signIn():
    return loginWithRealDb(otherdb)#login(db) #defined in the user login package

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
    app.run()

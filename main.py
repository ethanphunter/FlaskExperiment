"""
Author: Ethan Hunter
Comments: A simple Flask app for me to mess around with.
Note: I relieze that storing the user passwords the way I am is a very bad idea,
      I would never use this minimal of security in a real world app
"""

from flask import Flask, render_template, request, redirect, session, abort, jsonify
from Database import MyDatabase
from RealDatabase import Database
# from User import User
from UserLoginPackage import login, logout, requireLogin

db = MyDatabase()
otherdb = Database()
app = Flask(__name__)

# Set Debug to true for development purposes
# SECRET_KEY is used in the session object
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='A Very Very Secret Key'))

# def requireLogin():
#     if (not session.get("logged_in")):
#         return abort(401)

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
# I wouldn't use this for a real life system.
@app.route("/login", methods=["GET","POST"])
def signIn():
    return login(db)
# def login():
#     if (request.method == "POST"):
#         user = db.getUser(request.form["username"])
#         if (user == "no match"):
#             print("Error!!!")
#             abort(401)
#         else:
#             print("Checking password...")
#             if(user.verify_password(request.form["password"])):
#                 print("password is correct!")
#                 session['logged_in'] = True
#                 print("logged_in set")
#                 session["current_user"] = user.email
#                 print(user.email + " Logged in")
#                 return redirect("/")
#             else:
#                 print("Wrong password!!")
#                 abort(401)
#     else:
#         return render_template("login.html")

# Log the user out
@app.route("/logout")
def signOut():
    return logout()
# def logout():
#     session["current_user"] = None
#     print("Logged out")
#     session["logged_in"] = False
#     return render_template("logoutPage.html")

# You should only be able to access this if you are logged in
@app.route("/secret")
def secret():
    requireLogin()
    return "Current User: " + session.get("current_user")

if (__name__ == "__main__"):
    app.run()

"""
Author: Ethan Hunter
Comments: A simple Flask app for me to mess around with.
Note: I relieze that storing the user passwords the way I am is a very bad idea,
      I would never use this minimal of security in a real world app
"""

from flask import Flask, render_template, request, redirect, session, abort, jsonify
from Database import MyDatabase
from User import User

db = MyDatabase()
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

# This adds a new user to the Database
@app.route("/newUser", methods=["POST"])
def new_user():
    email = request.form["email"]
    #print(email)
    password = request.form["password"]
    #print(password)
    user = User(email, password)
    #print(user)
    db.addAUser(user)
    #print(password)
    print("new user: " + user.email)
    return redirect("/")

# Log a user in. This is a pretty simple way of doing it, but it works
# I wouldn't use this for a real life system.
@app.route("/login", methods=["GET","POST"])
def login():
    if (request.method == "POST"):
        user = db.getUser(request.form["username"])
        if (user == "no match"):
            print("Error!!!")
            abort(401)
        else:
            print("Checking password...")
            if(user.verify_password(request.form["password"])):
                print("password is correct!")
                session['logged_in'] = True
                print("logged_in set")
                session["current_user"] = user.email
                print(user.email + " Logged in")
                return redirect("/")
            else:
                print("Wrong password!!")
                abort(401)
    else:
        return render_template("login.html")

# Log the user out
@app.route("/logout")
def logout():
    session["current_user"] = None
    print("Logged out")
    session["logged_in"] = False
    return redirect("/")

# You should only be able to access this if you are logged in
@app.route("/secret")
def secret():
    if (not session.get("logged_in")):
        abort(401)
    return "Current User: " + session.get("current_user")

if (__name__ == "__main__"):
    app.run()

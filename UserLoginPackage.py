from flask import render_template, request, redirect, session, abort, jsonify
from User import User

loginHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
    <h2>Please Log In</h2>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"></input>
      password: <br>
      <input type="text" name="password"></input>
      <input type="submit" name="login">
    </form>
  </body>
</html>"""

logoutHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Logged Out</title>
  </head>
  <body>
    <h2>Logged Out</h2>
    <a href="/">home</a>
  </body>
</html>"""

def requireLogin():
    if (not session.get("logged_in")):
        return abort(401)

def login(db):
    if (request.method == "POST"):
        user = db.getUser(request.form["username"])
        if (user == "no match"):
            print("Error!!!")
            return abort(401)
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
                return abort(401)
    else:
        return loginHtml

def logout():
    session["current_user"] = None
    print("Logged out")
    session["logged_in"] = False
    return logoutHtml

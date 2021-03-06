from flask import render_template, request, redirect, session, abort, jsonify
from passlib.apps import custom_app_context as pwd_context

loginHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
      <a href="/">Home</a>
    <h2>Please Log In</h2>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"> <br>
      password: <br>
      <input type="password" name="password">
      <input type="submit" name="login">
    </form>
  </body>
</html>"""

badCredsHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
    <a href="/">Home</a>
    <h2>Please Log In</h2>
    <p style="color:red">
        Wrong username or password, please check your credentials and try again.
    </p>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"> <br>
      password: <br>
      <input type="password" name="password">
      <input type="submit" name="login">
    </form>
  </body>
</html>"""

lockedOutHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
    <a href="/">Home</a>
    <h2>Please Log In</h2>
    <p style="color:red">
        Error: Your account has been locked out for security reasons. Please contact the administrator to have your account unlocked.
    </p>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"> <br>
      password: <br>
      <input type="password" name="password">
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

def logout():
    if (not session["logged_in"]):
        return redirect("/")
    else:
        session["current_user"] = None
        print("Logged out")
        session["logged_in"] = False
        return logoutHtml

def loginWithRealDb(db):
        if (request.method == "POST"):
            username = request.form["username"]
            passwordHash = db.getUser(username)
            if (passwordHash == ""):
                print("No User Found")
                return badCredsHtml
            else:
                if (db.userIsLockedOut(username)[0][0]):
                    return lockedOutHtml
                else:
                    print("Checking password...")
                    if (pwd_context.verify(request.form["password"], passwordHash)):
                        db.updateNumberOfAttempts(username, 4)
                        print("password is correct!")
                        session['logged_in'] = True
                        print("logged_in set")
                        session["current_user"] = username
                        print(username + " Logged in")
                        session["friend_error"] = ""
                        return redirect("/")
                    else:
                        attempts = db.getNumberOfAttempts(username)[0][0]
                        if (attempts < 1 or attempts > 4):
                            db.lockOutUser(username)
                            db.enterLogMessage("User ~" + username + "~ is now locked out")
                        else:
                            db.updateNumberOfAttempts(username, attempts - 1)
                        print("Wrong password!!")
                        return badCredsHtml
        else:
            return loginHtml

def changePassword(db):
    username = session.get("current_user")
    passwordHash = db.getUser(username)
    oldPassword = request.form["old_password"]
    newPassword = request.form["new_password"]
    if (username == "uni"):
        return redirect("/gameList")
    if (passwordHash == ""):
        print("No User found while trying to change password")
        return abort(401)
    else:
        if (pwd_context.verify(oldPassword, passwordHash)):
            x = db.changePassword(username,pwd_context.encrypt(newPassword))
            if (x == None):
                print("password changed")
                db.enterLogMessage( "~" + username + "~ changed their password")
                return redirect("/userSettings")
            else:
                print("password change query error")
                db.enterLogMessage("Update Password Query Error for user: ~" + username + "~")
                return abort(500)
        else:
            print("Invalid old password")
            return redirect("/userSettings")

def encryptString(string):
    return pwd_context.encrypt(string)

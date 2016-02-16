from flask import Flask, render_template, request, redirect
from Database import MyDatabase

db = MyDatabase()
app = Flask(__name__)

#This is how you define a route
@app.route("/")
def index():
    #The return statement determines what html the user sees
    return render_template("index.html")

#In the html there is a form element that posts to this endpoint
#This route just prints the email that was submitted in the email input field
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

if (__name__ == "__main__"):
    app.run()

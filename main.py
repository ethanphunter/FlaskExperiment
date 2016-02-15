from flask import Flask, render_template, request, redirect
from Database import MyDatabase

db = MyDatabase()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["POST"])
def form():
    email = request.form["email"]
    print(email)
    return redirect("/")

@app.route("/search", methods=["POST"])
def search():
    results = [db.getById(str(request.form["id"]))]#["1",str(request.form["id"])]
    return render_template("searchResults.html", results = results)

#if (__name__ == "__main__"):
#    app.run()

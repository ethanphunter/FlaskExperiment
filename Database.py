import json
from User import User

class MyDatabase():

    def __init__(self):
        jsonFile = open("items.json", "r").read()
        jsonData = json.loads(jsonFile)
        x = {}
        for item in jsonData["items"]:
            x[str(item["id"])] = str(item["name"])
        self.items = x
        self.users = {}

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        return self.items

    def addAUser(self, user):
        self.users[user.getUserName()] = user
        return user

    def getUser(self, email):
        try:
            return self.users[email]
        except KeyError:
            return "no match"

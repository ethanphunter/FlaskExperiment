import json

class MyDatabase():

    def __init__(self):
        jsonFile = open("items.json", "r").read()
        jsonData = json.loads(jsonFile)
        x = {}
        for item in jsonData["items"]:
            x[str(item["id"])] = str(item["name"])
        self.items = x

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        return self.items

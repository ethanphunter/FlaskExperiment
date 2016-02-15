class MyDatabase():

    def __init__(self):
        self.items = {"1": "chips", "2": "soda"}

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

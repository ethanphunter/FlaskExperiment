#from flask import g

class User():

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def verify_password(self, password):
        return (password == self.password)

    def getPassword(self):
        return self.password

    def serialize(self):
        return {"username": self.email}

    def __str__(self):
        return self.email

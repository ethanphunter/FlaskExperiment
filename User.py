from passlib.apps import custom_app_context as pwd_context

class User(object):

    def __init__(self,name,password):
        self.userName = name
        self.password = self.hashPassword(password)

    def hashPassword(self, passw):
        return pwd_context.encrypt(passw)

    def verify_password(self, passw):
        return pwd_context.verify(passw, self.password)

    def getPassword(self):
        return self.password

    def getUserName(self):
        return self.userName

    def serialize(self):
        return {"username": self.userName}

    def __str__(self):
        return self.userName

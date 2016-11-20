class DatabaseResult(object):
    def __init__(self,value):
        self.value = value

    def get(self):
        return self.value

    def isSuccess(self):
        return False

    def isFailure(self):
        return False

    def getOrElse(self,elseValue):
        if (self.isFailure()):
            return elseValue
        else:
            return self.value


class Success(DatabaseResult):
    def __init__(self,value):
        super(Success,self).__init__(value)

    #@override
    def isSuccess(self):
        return not super(Success,self).isSuccess()


class Failure(DatabaseResult):
    def __init__(self,errorMessage):
        self.errorMessage = errorMessage
        super(Failure,self).__init__(None)

    #@override
    def isFailure(self):
        return not super(Failure,self).isFailure()

    def getErrorMessage(self):
        return self.errorMessage

import os

def getLines(fileName):
    fileData = open(fileName, "r")
    lines = []
    for line in fileData:
        lines.append(line.strip())
    fileData.close()
    return lines

def getDatabaseUrl():
    if (os.path.exists("secrets.txt")):
        return "dbname = 'FlaskExperimentDb' host = 'localhost'"
    elif (os.environ.get("TEST") != None):
        return "dbname = 'travis_ci_test' host = 'localhost' user = 'postgres'"
    else:
        return os.environ["DATABASE_URL"]

def getSecretKey():
    if (os.path.exists("secrets.txt")):
        lines = getLines("secrets.txt")
        return lines[1]
    else:
        return os.environ["SECRET_KEY"]

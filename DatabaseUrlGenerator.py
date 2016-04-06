import os

def getLines(fileName):
    fileData = open(fileName, "r")
    lines = []
    for line in fileData:
        lines.append(line.strip())
    fileData.close()
    return lines

def getDatabaseUrl():
    if (os.path.exists("databaseurl.txt")):
        lines = getLines("databaseurl.txt")
        return lines[0]
    else:
        return os.environ["DATABASE_URL"]

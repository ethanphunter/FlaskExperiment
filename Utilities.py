"""This file is for helper functions"""

flaskDelimiter = "~flask~"

def intifyList(aList):
    intedList = []
    for i in aList:
        intedList.append(int(i))
    return intedList

def listToCsvString(l):
    if (l == []):
        return ""
    elif (len(l) == 1):
        return str(head(l))
    else:
        return str(head(l)) + "," + listToCsvString(tail(l))

def csvToList(csv):
    return csv.split(",")

def toFlaskDelimitedString(l):
    if (l == []):
        return ""
    elif (len(l) == 1):
        return str(head(l))
    else:
        return str(head(l)) + flaskDelimiter + toFlaskDelimitedString(tail(l))

def fromFlaskDelimitedString(s):
    return s.split(flaskDelimiter)

def head(l):
    if (l == []):
        return []
    else:
        return l[0]

def tail(l):
    return l[1:]

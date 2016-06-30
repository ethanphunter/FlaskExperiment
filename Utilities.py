"""This file is for helper functions"""

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

def toFlaskDelimitedString(l):
    if (l == []):
        return ""
    elif (len(l) == 1):
        return str(head(l))
    else:
        return str(head(l)) + "~flask~" + toFlaskDelimitedString(tail(l))

def head(l):
    if (l == []):
        return []
    else:
        return l[0]

def tail(l):
    return l[1:]

class NoPiece(object):
    def __init__(self,row,col):
        self.row   = row
        self.col   = col
        self.color = ""
        self.name  = "NoPiece"

    def json(self):
        return {
            "row"   : self.row,
            "col"   : self.col,
            "color" : self.color,
            "name"  : self.name
        }

    def __str__(self):
        return ""


class Piece(object):
    def __init__(self,row,col,color,name):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.validSpaces = []

    def isValidMove(self,row,col):
        print(self.validSpaces)
        return (row,col) in self.validSpaces

    def calculateValidSpaces(self,board):
        return NotImplemented

    def setCords(self,row,col):
        self.row = row
        self.col = col

    def getColor(self):
        return self.color

    def __str__(self):
        return self.color + self.name

    def json(self):
        return {
            "row"   : self.row,
            "col"   : self.col,
            "color" : self.color,
            "name"  : self.name
        }

"""
-------------------------------
|         |         |         |
| x-1,y+1 | x,y+1   | x+1,y+1 |
|         |         |         |
-------------------------------
|         |         |         |
|  x-1,y  |   x,y   |  x+1,y  |
|         |         |         |
-------------------------------
|         |         |         |
| x-1,y-1 |  x,y-1  | x+1,y-1 |
|         |         |         |
-------------------------------
"""

def diagonal(x,y,board):
    spaces = []
    upLeftCords    = (y-1, x-1)
    upRightCords   = (y-1, x+1)
    downLeftCords  = (y+1, x-1)
    downRightCords = (y+1, x+1)
    if (insideBoard2(upLeftCords)):
        spaces.append(upLeftCords)
    if (insideBoard2(upRightCords)):
        spaces.append(upRightCords)
    if (insideBoard2(downLeftCords)):
        spaces.append(downLeftCords)
    if (insideBoard2(downRightCords)):
        spaces.append(downRightCords)
    return spaces

def diagonal2(x,y,board):
    spaces = []
    for i in range(0,8):
        upLeft = (y-i,x-i)
        if (insideBoard2(upLeft) and upLeft != (y,x)):
            if (board.getSpace(upLeft[0],upLeft[1]).isEmpty()):
                spaces.append(upLeft)
            else:
                spaces.append(upLeft)
                break

    for i in range(0,8):
        upRight = (y-i,x+i)
        if (insideBoard2(upRight) and upRight != (y,x)):
            if (board.getSpace(upRight[0],upRight[1]).isEmpty()):
                spaces.append(upRight)
            else:
                spaces.append(upRight)
                break

    for i in range(0,8):
        downLeft = (y+i,x-i)
        if (insideBoard2(downLeft) and downLeft != (y,x)):
            if (board.getSpace(downLeft[0],downLeft[1]).isEmpty()):
                spaces.append(downLeft)
            else:
                spaces.append(downLeft)
                break

    for i in range(0,8):
        downRight = (y+i,x+i)
        if (insideBoard2(downRight) and downRight != (y,x)):
            if (board.getSpace(downRight[0],downRight[1]).isEmpty()):
                spaces.append(downRight)
            else:
                spaces.append(downRight)
                break
    return spaces

def rightLeftUpDown(x,y,board):
    spaces     = []
    upCords    = (y-1,x)
    downCords  = (y+1,x)
    rightCords = (y,x+1)
    leftCords  = (y,x-1)
    if (insideBoard2(upCords)):
        spaces.append(upCords)
    if (insideBoard2(downCords)):
        spaces.append(downCords)
    if (insideBoard2(rightCords)):
        spaces.append(rightCords)
    if (insideBoard2(leftCords)):
        spaces.append(leftCords)
    return spaces

def rightLeftUpDown2(x,y,board):
    spaces = []
    for i in range(0,8):
        right = (y,x+i)
        if (insideBoard2(right) and right != (y,x)):
            if (board.getSpace(right[0],right[1]).isEmpty()):
                spaces.append(right)
            else:
                spaces.append(right)
                break

    for i in range(0,8):
        left = (y,x-i)
        if (insideBoard2(left) and left != (y,x)):
            if (board.getSpace(left[0],left[1]).isEmpty()):
                spaces.append(left)
            else:
                spaces.append(left)
                break
    for i in range(0,8):
        up = (y+i,x)
        if (insideBoard2(up) and up != (y,x)):
            if (board.getSpace(up[0],up[1]).isEmpty()):
                spaces.append(up)
            else:
                spaces.append(up)
                break
    for i in range(0,8):
        down = (y-i,x)
        if (insideBoard2(down) and down != (y,x)):
            if (board.getSpace(down[0],down[1]).isEmpty()):
                spaces.append(down)
            else:
                spaces.append(down)
                break
    return spaces

def knightMoves(x,y,board):
    spaces = []
    possibleSpaces = [
    (x-1,y+2),
    (x-2,y+1),
    (x-2,y-1),
    (x-1,y-2),
    (x+1,y+2),
    (x+2,y+1),
    (x+2,y-1),
    (x+1,y-2)]
    for space in possibleSpaces:
        if (insideBoard(space[0],space[1])):
            spaces.append(space)

    return spaces

def pawnSpaces(x,y,board,color):
    spaces = []
    if (color == "black"):
        forward = (y+1,x)
        attackLeft = (y+1,x-1)
        attackRight = (y+1,x+1)
        if (insideBoard2(forward)):
            if (board.getSpace(forward[0],forward[1]).isEmpty()):
                spaces.append(forward)
                if (y == 1):
                    doubleForward = (y+2,x)
                    if (insideBoard2(doubleForward)):
                        if (board.getSpace(doubleForward[0],doubleForward[1]).isEmpty()):
                            spaces.append(doubleForward)
        if (insideBoard2(attackLeft)):
            if (board.getSpace(attackLeft[0],attackLeft[1]).nonEmpty()):
                spaces.append(attackLeft)
        if (insideBoard2(attackRight)):
            if (board.getSpace(attackRight[0],attackRight[1]).nonEmpty()):
                spaces.append(attackRight)
    else:
        forward = (y-1,x)
        doubleForward = (y-2,x)
        attackLeft = (y-1,x+1)
        attackRight = (y-1,x-1)
        if (insideBoard2(forward)):
            if (board.getSpace(forward[0],forward[1]).isEmpty()):
                spaces.append(forward)
        if (y == 6):
            if (board.getSpace(doubleForward[0],doubleForward[1]).isEmpty()):
                spaces.append(doubleForward)
        if (insideBoard2(attackLeft)):
            if (board.getSpace(attackLeft[0],attackLeft[1]).nonEmpty()):
                spaces.append(attackLeft)
        if (insideBoard2(attackRight)):
            if (board.getSpace(attackRight[0], attackRight[1]).nonEmpty()):
                spaces.append(attackRight)
    return spaces


def insideBoard2(cords):
    return (0 <= cords[0] <= 7 and 0 <= cords[1] <= 7)

def insideBoard(x,y):
    return (0 <= x <= 7 and 0 <= y <= 7)

"""
####################################################################################
"""

class Pawn(Piece):

    def __init__(self,row,col,color):
        super(Pawn, self).__init__(row,col,color,"Pawn")

    def calculateValidSpaces(self,board):
        self.validSpaces = pawnSpaces(self.col,self.row,board,self.color)

"""
####################################################################################
"""

class King(Piece):
    def __init__(self,row,col,color):
        super(King, self).__init__(row,col,color,"King")

    def calculateValidSpaces(self,board):
        self.validSpaces = rightLeftUpDown(self.col,self.row,board)
        self.validSpaces = self.validSpaces + diagonal(self.col,self.row,board)

"""
####################################################################################
"""

class Queen(Piece):
    def __init__(self,row,col,color):
        super(Queen, self).__init__(row,col,color,"Queen")

    def calculateValidSpaces(self,board):
        self.validSpaces = rightLeftUpDown2(self.row,self.col,board)
        self.validSpaces = self.validSpaces + diagonal2(self.col,self.row,board)

"""
####################################################################################
"""

class Bishop(Piece):
    def __init__(self,row,col,color):
        super(Bishop, self).__init__(row,col,color,"Bishop")

    def calculateValidSpaces(self,board):
        self.validSpaces = diagonal2(self.col,self.row,board)

"""
####################################################################################
"""

class Knight(Piece):
    def __init__(self,row,col,color):
        super(Knight, self).__init__(row,col,color,"Knight")

    def calculateValidSpaces(self,board):
        self.validSpaces = knightMoves(self.row,self.col,board)

"""
####################################################################################
"""

class Rook(Piece):
    def __init__(self,row,col,color):
        super(Rook, self).__init__(row,col,color,"Rook")

    def calculateValidSpaces(self,board):
        self.validSpaces = rightLeftUpDown2(self.col,self.row,board)

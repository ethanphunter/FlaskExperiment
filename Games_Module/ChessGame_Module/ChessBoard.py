from ChessPieces import *

"""
####################################################################################
"""

class ChessBoard(object):
    """
    setupBoard()
    makeMove(fromRow,fromCol,toRow,toCol)
    getSpace(row,col)
    gameOver()
    getWinner()
    whoseTurn()
    getAsList()
    """
    def __init__(self):
        self.board = self.setupBoard()
        self.isGameOver = False
        self.winnerColor = None
        self.whoseTurnColor = "white"

    def setupBoard(self):
        board = []
        for row in range(0,8):
            column = []
            for col in range(0,8):
                column.append(self.getStartingSpace(row,col))
            board.append(column)
        self.board = board
        self.calculateMoves()
        return board

    def getStartingSpace(self,row,col):
        if (row == 1):
            return ChessBoardSpace(Pawn(row,col,"black"))
        elif (row == 6):
            return ChessBoardSpace(Pawn(row,col,"white"))
        elif (row == 0 and col == 3):
            return ChessBoardSpace(King(row,col,"black"))
        elif (row == 7 and col == 4):
            return ChessBoardSpace(King(row,col,"white"))
        elif (row == 0 and col == 4):
            return ChessBoardSpace(Queen(row,col,"black"))
        elif (row == 7 and col == 3):
            return ChessBoardSpace(Queen(row,col,"white"))
        elif (row == 0 and (col == 2 or col == 5)):
            return ChessBoardSpace(Bishop(row,col,"black"))
        elif (row == 7 and (col == 2 or col == 5)):
            return ChessBoardSpace(Bishop(row,col,"white"))
        elif (row == 0 and (col == 1 or col == 6)):
            return ChessBoardSpace(Knight(row,col,"black"))
        elif (row == 7 and (col == 1 or col == 6)):
            return ChessBoardSpace(Knight(row,col,"white"))
        elif (row == 0 and (col == 0 or col == 7)):
            return ChessBoardSpace(Rook(row,col,"black"))
        elif (row == 7 and (col == 0 or col == 7)):
            return ChessBoardSpace(Rook(row,col,"white"))
        else:
            return ChessBoardSpace(NoPiece(row,col))

    def getStartingSpaceDebuging(self,row,col):
        if (row == 1 and col == 1):
            return ChessBoardSpace(Pawn(row,col,"black"))
        elif (row == 6 and col == 1):
            return ChessBoardSpace(Pawn(row,col,"white"))
        else:
            return ChessBoardSpace(NoPiece(row,col))

    def calculateMoves(self):
        for row in self.getAsList():
            for col in row:
                piece = col.getPiece()
                if (not isinstance(piece, NoPiece)):
                    piece.calculateValidSpaces(self)

    def makeMove(self,fromRow,fromCol,toRow,toCol):
        fromSpace = self.getSpace(fromRow,fromCol)
        toSpace = self.getSpace(toRow,toCol)
        if (fromSpace.isEmpty()):
            return "Error Empty From Space"
        elif (fromSpace.getPiece().getColor() == self.whoseTurn()):
            print("From: " + str(fromRow) + ":" + str(fromCol))
            print(toRow,toCol)
            print(fromSpace.getPiece().getColor() + ":" + self.whoseTurn())
            print(fromSpace.getPiece().validSpaces)
            print("====================")
            if (fromSpace.getPiece().isValidMove(toRow,toCol)):
                toSpace.setPiece(fromSpace.getPiece())
                fromSpace.getPiece().setCords(toRow,toCol)
                fromSpace.setPiece(NoPiece(fromRow,fromCol))
                self.checkGameStatus()
                if (not self.gameOver()):
                    self.calculateMoves()
                    self.changeTurn()
                    return ""
                else:
                    return "Game Over"
            else:
                return "Error Invalid To Space"
        else:
            return "Error Not Your Piece"

    def changeTurn(self):
        if (self.whoseTurn() == "white"):
            self.whoseTurnColor = "black"
        else:
            self.whoseTurnColor = "white"

    def getSpace(self,row,col):
        return self.board[row][col]

    def gameOver(self):
        return self.isGameOver

    def getWinner(self):
        return self.winnerColor

    def whoseTurn(self):
        return self.whoseTurnColor

    def checkGameStatus(self):
        kings = []
        for row in self.board:
            for col in row:
                if (isinstance(col.getPiece(), King)):
                    kings.append(col.getPiece())
        if (len(kings) == 1):
            self.isGameOver = True
            self.winnerColor = kings[0].getColor()

    def getAsList(self):
        return self.board

    def jsonBoard(self):
        board = []
        for row in self.getAsList():
            c = []
            for col in row:
                c.append(col.json())
            board.append(c)
        return board


    def json(self):
        return {
            "board"          : self.jsonBoard(),
            "isGameOver"     : self.isGameOver,
            "winnerColor"    : self.winnerColor,
            "whoseTurnColor" : self.whoseTurnColor
        }

    def decodeBoard(self,json):
        board = []
        rowIndex = 0
        for row in json:
            column = []
            colIndex = 0
            for col in row:
                emptySpace = ChessBoardSpace(NoPiece(rowIndex,colIndex))
                emptySpace.decode(col)
                column.append(emptySpace)
                colIndex += 1
            board.append(column)
            rowIndex += 1
        self.board = board
        self.calculateMoves()

    def decode(self, json):
        self.decodeBoard(json["board"])
        self.isGameOver = json["isGameOver"]
        self.winnerColor = json["winnerColor"]
        self.whoseTurnColor = json["whoseTurnColor"]

"""
####################################################################################
"""

class ChessBoardSpace(object):
    """
    isEmpty()
    getPiece()
    setPiece(piece)
    """
    def __init__(self,piece):
        self.piece = piece

    def isEmpty(self):
        return (isinstance(self.piece, NoPiece))

    def nonEmpty(self):
        return not self.isEmpty()

    def getPiece(self):
        return self.piece

    def setPiece(self,piece):
        self.piece = piece

    def __str__(self):
        return str(self.piece)

    def json(self):
        return {
            "piece" : self.piece.json()
        }

    def decode(self, json):
        json = json["piece"]
        name = json["name"]
        row = json["row"]
        col = json["col"]
        color = json["color"]
        if (name == "Pawn"):
            self.piece = Pawn(row,col,color)
        elif (name == "King"):
            self.piece = King(row,col,color)
        elif (name == "Queen"):
            self.piece = Queen(row,col,color)
        elif (name == "Bishop"):
            self.piece = Bishop(row,col,color)
        elif (name == "Knight"):
            self.piece = Knight(row,col,color)
        elif (name == "Rook"):
            self.piece = Rook(row,col,color)
        else:
            self.piece = NoPiece(row,col)

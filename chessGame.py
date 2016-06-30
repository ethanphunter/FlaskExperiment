"""a user will have a list of game ids that they will be a part of
    a game will have an id, two usernames, whose turn it is, and the board state"""

"""
TODO:
Work on storing the game in the db
"""

from Game import Game
from ChessPieces import *
from ChessBoard import *
from flask import request, redirect, session, abort

# columnLetters = ["a","b","c","d","e","f","g","h"]

# def newBoard():
#     x = []
#     for row in range(0,8):
#         y = []
#         for col in range(0,8):
#             y.append("")
#         x.append(y)
#     return x
#
# def setupBoard():
#     board = newBoard()
#     for row in range(0,8):
#         if (row == 1):
#             for col in range(0,8):
#                 board[row][col] = Pawn(row,col,"black")
#         elif (row == 6):
#             for col in range(0,8):
#                 board[row][col] = Pawn(row,col,"white")
#     return board
#
# def newGame():
#     session["board"] = stringifyBoard(setupBoard())
#
# def stringifyBoard(board):
#     stringifiedBoard = []
#     for row in board:
#         stringedRow = []
#         for col in row:
#             stringedRow.append(str(col))
#         stringifiedBoard.append(stringedRow)
#     return stringifiedBoard
#
# def unStringifyBoard(board):
#     unStringifiedBoard = []
#     rowI = 0
#     for row in board:
#         unStringedRow = []
#         colI = 0
#         for col in row:
#             if ("Pawn" in col):
#                 unStringedRow.append(Pawn(rowI,colI,col.split(" ")[0]))
#             else:
#                 unStringedRow.append("")
#             colI += 1
#         rowI += 1
#         unStringifiedBoard.append(unStringedRow)
#     calculateValidMoves(unStringifiedBoard)
#     return unStringifiedBoard
#
# def calculateValidMoves(board):
#     for row in board:
#         for col in row:
#             if (col != ""):
#                 col.calculateValidSpaces(board)


class ChessGame(Game):
    def __init__(self,anId,players):
        self.board = ChessBoard()
        self.whiteUserName = players[0]
        self.blackUserName = players[1]
        self.whoseTurn = players[0]
        self.columnLetters = ["a","b","c","d","e","f","g","h"]
        super(ChessGame, self).__init__(anId,"ChessGame",players)

    def makeMove(self,fromRow,fromCol,toRow,toCol):
        fromCol = self.columnLetters.index(fromCol)
        toCol   = self.columnLetters.index(toCol)
        errorMessage = self.board.makeMove(fromRow,fromCol, toRow, toCol)
        if (errorMessage == ""):
            self.changeTurn()
            return ""
        else:
            return errorMessage

    def changeTurn(self):
        if (self.whoseTurn == self.players[0]):
            self.whoseTurn = self.players[1]
        else:
            self.whoseTurn = self.players[0]
        super(ChessGame, self).changeTurn(self.whoseTurn)

    def getBoardAsList(self):
        return self.board.getAsList()

    def json(self):
        return {
            "chessGame": {
                "gameId"    : self.getId(),
                "board"     : self.board.json(),
                "players"   : self.players,
                "whoseTurn" : self.whoseTurn
            }
        }

    def decode(self,json):
        self.board.decode(json["board"])
        self.players       = json["players"]
        self.whoseTurn     = json["whoseTurn"]
        self.whiteUserName = self.players[0]
        self.blackUserName = self.players[1]
        super(ChessGame, self).decode(json["gameId"],self.players,self.whoseTurn)

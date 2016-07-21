"""a user will have a list of game ids that they will be a part of
    a game will have an id, two usernames, whose turn it is, and the board state"""

from Games_Module.Game import Game
from ChessPieces import *
from ChessBoard import *
from flask import request, redirect, session, abort


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

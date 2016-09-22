from flask.json import JSONEncoder, JSONDecoder
from ChessGame_Module.ChessGame import ChessGame
from ChessGame_Module.ChessBoard import *
from ChessGame_Module.ChessPieces import *

class GameJSONEncoder(JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, Piece)):
            return obj.json()
        elif (isinstance(obj, NoPiece)):
            return obj.json()
        elif (isinstance(obj, ChessGame)):
            return obj.json()
        elif (isinstance(obj, ChessBoard)):
            return obj.json()
        elif (isinstance(obj, ChessBoardSpace)):
            return obj.json()
        else:
            return super(GameJSONEncoder, self).default(obj)

class GameJSONDecoder(object):
    def __init__(self):
        pass

    def decode(self, obj):
        if ("chessGame" not in obj):
            return ""
        else:
            game = ChessGame("",["",""])
            x = game.decode(obj["chessGame"])
            return game

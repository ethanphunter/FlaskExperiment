from flask.json import JSONEncoder, JSONDecoder
from chessGame import *
from ChessBoard import *
from ChessPieces import *

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
        # self.j = JSONDecoder(object_hook=self.object_hook)

    def decode(self, obj):
        # print(obj)
        # if "board" not in obj:
            # return super(GameJSONDecoder, self).decode(obj)
        # else:
            # aType = obj,
            # if (aType == "ChessGame"):
                # print("YESSSSSSSSSSS: " + aType)
            # return "obj[]"
        if ("chessGame" not in obj):
        # print(obj)
            # return super(GameJSONDecoder, self).decode(obj)
            return ""
        else:
            # print("YESSSSSSSSSSS")
            game = ChessGame("",["",""])
            # print("Yes")
            x = game.decode(obj["chessGame"])
            # print("Yeah")
            return game
            # return super(GameJSONDecoder, self).decode(obj)

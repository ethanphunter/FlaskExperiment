from flask import Blueprint, render_template, session, request, redirect
from UserLoginPackage import requireLogin

def ChessGameBluePrintConstructor(dbutils,gameJsonDecoder):
    ChessGameBluePrint = Blueprint("ChessGame",__name__,template_folder="templates")

    @ChessGameBluePrint.route("/board")
    def board():
        requireLogin()
        gameId = session.get("gameId")#request.args["gameId"]
        # print("Session gameId: " + gameId)
        game = dbutils.getGame(gameId)
        # print("Got game")
        session["chessGame"] = game #gameJsonDecoder.decode(session.get("chessGame"))
        return render_template("ChessBoard.html", game = game, error = session.get("BoardError"), userName = session.get("current_user"))

    @ChessGameBluePrint.route("/closeError")
    def closeError():
        session["BoardError"] = ""
        return redirect("/board")

    @ChessGameBluePrint.route("/makeMove", methods=["POST"])
    def makeMove():
        session["BoardError"] = ""
        fromRow = int(request.form["from-row"]) - 1
        fromCol = request.form["from-col"]
        toRow = int(request.form["to-row"]) - 1
        toCol = request.form["to-col"]
        game = gameJsonDecoder.decode(session.get("chessGame"))
        if (game.isPlayersTurn(session.get("current_user"))):
            error = game.makeMove(fromRow,fromCol,toRow,toCol)
            if (error != ""):
                session["BoardError"] = error
                print("There was a board error")
            else:
                session["chessGame"] = game
                print("Updating game in the db...")
                dbutils.updateGame(game)
                print("Game updated")
        else:
            session["BoardError"] = "Not Your Turn!"
        return redirect("/board")

    return ChessGameBluePrint

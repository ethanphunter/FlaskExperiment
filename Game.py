class Game(object):
    """Game class to be subclassed by every game.
    Constructor:
    Game(anId: string, name: string, players: List[String])
    """
    def __init__(self,anId,gameName,players):
        self.id = anId
        self.gameName = gameName
        self.players = players
        self.whoseTurn = players[0]

    def getId(self):
        return self.id

    def getName(self):
        return self.gameName

    def getPlayers(self):
        return self.players

    def getOtherPlayer(self,username):
        if (self.players[0] == username):
            return self.players[1]
        else:
            return self.players[0]

    def isPlayersTurn(self,userName):
        return (self.whoseTurn == userName)

    def getWhoseTurn(self):
        return self.whoseTurn

    def changeTurn(self,player):
        self.whoseTurn = player

    def json(self):
        return NotImplemented

    def decode(self,gameId,players,whoseTurn):
        self.players = players
        self.whoseTurn = whoseTurn
        self.id = gameId

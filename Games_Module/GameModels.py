class GameDetails(object):
    """
    Description: A object to hold minimal information about a game.
    """

    def  __init__(self, gameId, gameName, players, turn):
        self.gameId   = gameId
        self.gameName = gameName
        self.players  = players
        self.turn     = turn

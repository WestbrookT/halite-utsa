"""Andrew's Halite bot. Version name: alpha"""
from hlt import GameMap, Location, Move, Site
from networking import getInit, getFrame, sendFrame, sendInit, random

def calculateMove(x, y):
    return random.choice([0, 1, 2, 3, 4])

# Beginning of the game
myID, gameMap = getInit()
# We have 15 seconds to plan and preprocess before we call sendInit()


# Tells the game that we are ready
sendInit("AndrewBot: alpha")

# Game loop: runs one iteration per frame (or, "turn")
while True:
    moves = []
    # Begin the turn. We have 1 second to call sendFrame with our moves
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == myID:
                moves.append(Move(Location(x, y), calculateMove(x, y)))
    # Send our moves to the server and end our turn
    sendFrame(moves)

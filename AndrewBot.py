"""Andrew's Halite bot. Version name: alpha"""
from hlt import *
from networking import getInit, getFrame, sendFrame, sendInit, random

# Bot name
BOT_NAME = "AndrewBot"

def getCoordinatesOfDirection(origX, origY, direction):
    """Returns a tuple (x, y) of the location in the given direction."""
    if direction == NORTH:
        return (origX, origY + 1)
    elif direction == EAST:
        return (origX + 1, origY)
    elif direction == SOUTH:
        return (origX, origY - 1)
    elif direction == WEST:
        return (origX - 1, origY)

def preprocessGrid(gameMap):
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            site = gameMap.getSite(Location(x, y))
            logFile.write(str(int(site.production / site.strength * 200)) + " ")
        logFile.write("\n")

def getMove(x, y):
    """Returns the "optimal" move of our unit at (x, y).

    The unit at (x, y) should belong to us.

    Args:
        x: x cooridnate of the given unit square
        y: y coordinate of the given unit square

    Returns:
        A number in the range [0, 4] representing our desired move.
        0 => STILL
        1 => NORTH
        2 => EAST
        3 => SOUTH
        4 => WEST
    """
    mySite = gameMap.getSite(Location(x, y))
    highestSiteValue = -1
    highestSiteCardinal = 1
    for cardinal in CARDINALS:
        tx, ty = getCoordinatesOfDirection(x, y, cardinal)
        if getSiteValue(tx, ty) > highestSiteValue:
            highestSiteCardinal = cardinal
            highestSiteValue = getSiteValue(tx, ty)

    return highestSiteCardinal

def getSiteValue(x, y):
    site = gameMap.getSite(Location(x, y))
    return site.production / site.strength

# Beginning of the game. We have 15 seconds to plan and preprocess before we
# call sendInit()
myID, gameMap = getInit()
logFile = open(BOT_NAME + "-log.txt", "w")

preprocessGrid(gameMap)

# Tells the game that we are ready
sendInit(BOT_NAME)

# Game loop: runs one iteration per frame (or, "turn")
while True:
    moves = []
    # Begin the turn. We have 1 second to call sendFrame with our moves
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == myID:
                moves.append(Move(Location(x, y), getMove(x, y)))
    # Send our moves to the server and end our turn
    sendFrame(moves)

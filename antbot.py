from hlt import *
from networking import *

myID, gameMap = getInit()


f = open('log.txt', 'w')

# from net import Network
#
# layers = [10, 20, 20, 5]
# net = Network(layers)

height = gameMap.height
width = gameMap.width
p_grid = [[0]*height for i in range(width)]
def X(i):
    if i >= width:
        i -= width
    elif i < 0:
        i += width
    return i

def Y(i):
    if i >= height:
        i -= height
    elif i < 0:
        i += height
    return i

def direct(x, y, d):

    return [(x, y), (X(x), Y(y-1)), (X(x+1), y), (x, Y(y+1)), (X(x-1), Y(y))][d]

def move(x, y):
    site = gameMap.getSite(Location(x, y))
    if site.strength > 150:
        p_grid[x][y] -= 5
        if site.strength > 200:
            p_grid[x][y] = 2



    locs = [(x, y), (X(x), Y(y-1)), (X(x+1), y), (x, Y(y+1)), (X(x-1), Y(y))]


    best = 1
    p_max = p_grid[locs[1][0]][locs[1][1]]
    easy = False
    edge = False


    for i, loc in enumerate(locs):
        if i == 0:
            continue
        tsite = gameMap.getSite(Location(loc[0], loc[1]))

        tx, ty = loc[0], loc[1]

        if tsite.owner != myID:
            edge = True

        if tsite.strength <= site.strength and tsite.owner != myID:
            f.write("other: {}, mine: {}\n".format(tsite.strength, site.strength))
            best = i
            easy = True
            continue
            # p_grid[x][y] += 3
            # tx, ty = direct(x, y, i)
            # p_grid[tx][ty] += 5
            # return i
        elif not easy and p_max < p_grid[tx][ty]:
            best = i
            p_max = p_grid[tx][ty]

    if site.strength < 10 and not easy:
        p_grid[x][y] += 0
        return 0

    if easy:
        p_grid[x][y] += -10
        tx, ty = direct(x, y, i)
        p_grid[tx][ty] = p_grid[x][y] + 10

    tx, ty = direct(x, y, best)
    if edge and not easy:

        p_grid[x][y] += 15
        for loc in locs:
            tx, ty = loc[0], loc[1]
            p_grid[tx][ty] += 3

        return 0
    p_grid[tx][ty] += 1
    return best


def decay(arr):

    for y in range(height):
        for x in range(width):
            if arr[x][y] > 0:
                arr[x][y] -= 1


sendInit("AntBot")
while True:
    moves = []
    gameMap = getFrame()

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            p_grid[x][y] -= 1
            loc = gameMap.getSite(Location(x, y))
            if loc.owner == myID:
                moves.append(Move(Location(x, y), move(x, y)))
            else:
                p_grid[x][y] = loc.production







                #moves.append(Move(Location(x, y), int(random.random() * 5)))
    sendFrame(moves)

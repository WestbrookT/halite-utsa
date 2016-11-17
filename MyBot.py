from hlt import *
from networking import *

myID, gameMap = getInit()


f = open('log.txt', 'w')

# from net import Network
#
# layers = [10, 20, 20, 5]
# net = Network(layers)

height = 30
width = 30

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


def move(x, y):

    up = lup(x, y, 1)
    up1 = (up[0] - up[1])*up[2]

    r = lr(x, y, 1)
    r1 = (r[0] - r[1])*r[2]

    l = ll(x, y, 1)
    l1 = (l[0] - l[1])*l[2]

    d = ldown(x, y, 1)
    d1 = (d[0] - d[1])*d[2]

    opts = {1: up1, 2:r1, 3:d1, 4:l1}
    chk = {1: up, 2:r, 3:d, 4:l}

    val = up1
    max = 1

    for i in opts:
        if opts[i] > val:
            val = opts[i]
            max = i

    f.write("{} {}\n".format(x, y))



    # if max == 2:
    #     x += 1
    # elif max == 4:
    #     x -= 1
    # elif max == 1:
    #     y -= 1
    # elif max == 3:
    #     y += 1



    loc = Location(X(x), Y(y))
    site = gameMap.getSite(loc)
    f.write("{} {}, {} {} --\n".format(x, y, chk[max][1], site.strength/255*15))
    if chk[max][1] > site.strength/255*15:
        return 0
    return max



def lup(x, y, dis):
    prod = 0
    stren = 0
    own = 0
    count = 0
    for i in range(x-dis, x+dis):
        count += 1
        loc = Location(X(i), Y(y+dis))
        site = gameMap.getSite(loc)

        own += site.owner if site.owner != myID else -1
        prod += site.production
        stren += site.strength/255 * 15

    return (prod / count, stren / count, own / count)


def lr(x, y, dis):
    prod = 0
    stren = 0
    own = 0
    count = 0
    for i in range(y - dis, y + dis):
        count += 1
        loc = Location(X(x + dis), Y(i))
        site = gameMap.getSite(loc)

        own += site.owner if site.owner != myID else -1
        prod += site.production
        stren += site.strength / 255 * 15

    return (prod / count, stren / count, own / count)

def ll(x, y, dis):
    prod = 0
    stren = 0
    own = 0
    count = 0
    for i in range(y - dis, y + dis):
        count += 1
        loc = Location(X(x - dis), Y(i))
        site = gameMap.getSite(loc)

        own += site.owner if site.owner != myID else -1
        prod += site.production
        stren += site.strength / 255 * 15

    return (prod / count, stren / count, own / count)

def ldown(x, y, dis):
    prod = 0
    stren = 0
    own = 0
    count = 0
    for i in range(x - dis, x + dis):
        count += 1
        loc = Location(X(i), Y(y - dis))
        site = gameMap.getSite(loc)

        own += site.owner if site.owner != myID else -1
        prod += site.production
        stren += site.strength / 255 * 15

    return (prod / count, stren / count, own / count)







sendInit("MyPythonBot")
while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == myID:
                moves.append(Move(Location(x, y), move(x, y)))






                #moves.append(Move(Location(x, y), int(random.random() * 5)))
    sendFrame(moves)

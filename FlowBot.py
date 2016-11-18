from hlt import *
from networking import *
from random import randint

myID, gameMap = getInit()


f = open('grid.txt', 'w')

def log_grid(f, grid):

    h = len(grid[0])
    w = len(grid)
    f.write('\n')
    for y in range(h):
        out = ''
        for x in range(w):
            out += str(p_grid[x][y]) + ' '
        out += '\n'
        f.write(out)


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



    locs = [(x, y), (X(x), Y(y-1)), (X(x+1), y), (x, Y(y+1)), (X(x-1), Y(y))]

    max_p = 0
    best_dir = randint(1, 4)
    easy = False
    edge = False
    max_f = 0

    for d, loc in enumerate(locs):
        tx, ty = loc[0], loc[1]
        tsite = gameMap.getSite(Location(tx, ty))

        if tsite.owner != myID:
            if tsite.strength <= site.strength:
                if tsite.production >= max_p:
                    max_p = tsite.production
                    best_dir = d
                easy = True
            edge = True

        if not edge:
            if d == 0:
                continue
            if p_grid[tx][ty] > max_f:
                max_f = p_grid[tx][ty]
                best_dir = d

    if easy:
        tx, ty = direct(x, y, best_dir)
        p_grid[tx][ty] = p_grid[x][y]+1
        return best_dir

    if site.strength < site.production*2:
        return 0

    if edge and not easy:
        #Check diagonals in here



        return 0
    return best_dir




sendInit("flow")
while True:
    log_grid(f, p_grid)
    moves = []
    gameMap = getFrame()

    for y in range(gameMap.height):
        for x in range(gameMap.width):

            loc = gameMap.getSite(Location(x, y))
            if loc.owner == myID:

                moves.append(Move(Location(x, y), move(x, y)))
            else:
                #p_grid[x][y] = 0
                pass







                #moves.append(Move(Location(x, y), int(random.random() * 5)))
    sendFrame(moves)
f.close()
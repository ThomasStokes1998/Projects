from RubiksCube import Cube

rc = Cube()

# Variables
rotations = rc.rotations
letters = "ABCDEFGHIJKLMNOPQRSTUVWX"
corner_pieces = [[0, 4, 17], [1, 13, 16], [2, 9, 12], [3, 5, 8], [6, 11, 20], [10, 15, 21], [14, 19, 22], [7, 18, 23]]
edge_pieces = [[0, 16], [1, 12], [2, 8], [3, 4], [9, 15], [5, 11], [13, 19], [7, 17], [6, 23], [10, 20], [14, 21],
               [18, 22]]
parity = [[0, 16], [2, 8], [1, 12], [3, 4], [9, 15], [5, 11], [13, 19], [7, 17], [6, 23], [10, 20], [14, 21], [18, 22]]


def solvedPieces(scramble, prevstate=None, pieces=False, par=False):
    if prevstate is None:
        prevstate = rc.solved
    state = rc.move_sim(scramble, prevstate)
    corners = state[0]
    edges = state[1]
    centres = state[2]
    if pieces:
        corlist = []
        edglist = []
    sp = 0
    # Corners
    for cp in corner_pieces:
        solved = True
        for c in cp:
            if corners[c] // 4 != centres[c] // 4:
                solved = False
                break
        if solved:
            sp += 1
            if pieces:
                corlist.append(cp)
    # Edges
    e_pieces = edge_pieces
    if par:
        e_pieces = parity
    for ed in e_pieces:
        solved = True
        for e in ed:
            # If parity and two swapped pieces are already in the correct location
            if par and e in [8, 12] and edges[e] // 4 != 5 - centres[e] // 4:
                solved = False
                break
            elif par and e in [1, 2] and edges[e] // 4 != centres[e] // 4:
                solved = False
                break
            if not par or e not in [1, 2, 8, 12]:
                if edges[e] // 4 != centres[e] // 4:
                    solved = False
                    break
        if solved:
            sp += 1
            if pieces:
                edglist.append(ed)
    if pieces:
        return corlist, edglist
    return sp


def compareState(centres):
    for i in range(6):
        if centres[4 * i] // 4 != i:
            return False
    return True


def getCornerId(i):
    for j in range(8):
        if i in corner_pieces[j]:
            return j


def getEdgeId(i, par=False):
    if par:
        pieces = parity
    else:
        pieces = edge_pieces
    for j in range(12):
        if i in pieces[j]:
            return j


def blindletters(scramble, prevstate=None, letterscheme=letters):
    if prevstate is None:
        prevstate = rc.solved
    # Orient the scramble so white is on top and green is on front
    centres = rc.move_sim(scramble, prevstate)[2]
    if compareState(centres):
        nscramble = scramble
    else:
        for r in rc.rotations:
            ncentres = rc.move_sim(scramble + r, prevstate)[2]
            if compareState(ncentres):
                nscramble = scramble + r
                break
    state = rc.move_sim(nscramble, prevstate)
    corners = state[0]
    edges = state[1]
    cp, ep = solvedPieces(nscramble, prevstate, True)
    # Keep track of solved corners and edges
    traced_corners = [0] * 8
    traced_edges = [0] * 12

    # Corners
    # Solved Corners
    for c in cp:
        for i in range(8):
            if c[0] in corner_pieces[i]:
                traced_corners[i] = 1
    corner_memo = ""
    initcp = 2  # UFR Buffer
    buffer = initcp
    t = initcp
    count = 0
    while sum(traced_corners) < 8:
        # Incase an infinite loop is created
        count += 1
        if count == 100:
            print(traced_corners)
            return corner_memo, ""
        # Finds where the piece needs to go
        t = corners[t]
        # If buffer piece is found
        if getCornerId(t) == getCornerId(buffer):
            if len(corner_memo) > 0:
                if buffer != initcp:
                    corner_memo += letterscheme[t]
                traced_corners[getCornerId(buffer)] = 1
            # Checks if the first buffer is the last unsolved piece
            if sum(traced_corners) == 7 and traced_corners[getCornerId(initcp)] == 0:
                break
            # Finds the next valid corner piece
            for c in [0, 1, 3, 20, 21, 22, 23]:
                if traced_corners[getCornerId(c)] != 1:
                    t = c
                    buffer = c
                    corner_memo += letterscheme[t]
                    break
        else:
            if sum(traced_corners) < 8:
                corner_memo += letterscheme[t]
                traced_corners[getCornerId(t)] = 1

    # Edges
    # Adjust Edges to aviod parity
    par = False
    if len(corner_memo) % 2 == 1:
        par = True
    cp, ep = solvedPieces(nscramble, prevstate, True, par)
    # Solved Edges
    pieces = edge_pieces
    if par:
        pieces = parity
    for e in ep:
        for i in range(12):
            if e[0] in pieces[i]:
                traced_edges[i] = 1
    edge_memo = ""
    initep = 2  # UF Buffer
    buffer = initep
    t = initep
    count = 0
    while sum(traced_edges) < 12:
        # Incase an infinite loop is created
        count += 1
        if count == 100:
            print(traced_edges)
            return corner_memo, edge_memo
        # Finds where the piece needs to go
        t = edges[t]
        # Parity
        if par and t in [1, 2]:
            t = 3 - t
        if par and t in [12, 8]:
            t = 20 - t
        # If buffer piece is found
        if getEdgeId(t, par) == getEdgeId(buffer, par):
            if len(edge_memo) > 0:
                if buffer != initep:
                    edge_memo += letterscheme[t]
                traced_edges[getEdgeId(buffer, par)] = 1
            # Checks if the first buffer is the last unsolved piece
            if sum(traced_edges) == 11 and traced_edges[getEdgeId(initcp, par)] == 0:
                break
            # Finds the next valid edge piece
            for c in [0, 1, 2, 3, 9, 11, 17, 19, 20, 21, 22, 23]:
                if traced_edges[getEdgeId(c, par)] != 1 and c != initep:
                    t = c
                    # Swaps to new buffer
                    buffer = c
                    edge_memo += letterscheme[t]
                    break
        else:
            if sum(traced_edges) < 12:
                edge_memo += letterscheme[t]
                traced_edges[getEdgeId(t, par)] = 1
    return corner_memo, edge_memo


if __name__ == "__main__":
    scramble = rc.scramble()
    cm, em = blindletters(scramble)
    print(scramble)
    print("Corners: " + cm + "\nEdges: " + em)
    rc.viscube(scramble)

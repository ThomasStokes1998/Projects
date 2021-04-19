import numpy as np
import matplotlib.pyplot as plt

# Solved Cube
solved = np.array([np.arange(0, 24, 1), np.arange(0, 24, 1)])
# Generators
# move[0]=Corners, move[1]=Edges
left = np.array([[18, 1, 2, 17, 7, 4, 5, 6, 0, 9, 10, 3, 12, 13, 14, 15, 16, 23, 20, 19, 8, 21, 22, 11],
                 [0, 1, 2, 17, 7, 4, 5, 6, 8, 9, 10, 3, 12, 13, 14, 15, 16, 23, 18, 19, 20, 21, 22, 11]])
left_ = np.array([[8, 1, 2, 11, 5, 6, 7, 4, 20, 9, 10, 23, 12, 13, 14, 15, 16, 3, 0, 19, 18, 21, 22, 17],
                  [0, 1, 2, 11, 5, 6, 7, 4, 8, 9, 10, 23, 12, 13, 14, 15, 16, 3, 18, 19, 20, 21, 22, 17]])
right = np.array([[0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23],
                  [0, 9, 2, 3, 4, 5, 6, 7, 8, 21, 10, 11, 15, 12, 13, 14, 16, 17, 18, 1, 20, 19, 22, 23]])
right_ = np.array([[0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23],
                   [0, 19, 2, 3, 4, 5, 6, 7, 8, 1, 10, 11, 13, 14, 15, 12, 16, 17, 18, 21, 20, 9, 22, 23]])
up = np.array([[3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23],
               [3, 0, 1, 2, 8, 5, 6, 7, 12, 9, 10, 11, 16, 13, 14, 15, 4, 17, 18, 19, 20, 21, 22, 23]])
up_ = np.array([[1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23],
                [1, 2, 3, 0, 16, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 20, 21, 22, 23]])
down = np.array([[0, 1, 2, 3, 4, 5, 18, 19, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 23, 20, 21, 22],
                 [0, 1, 2, 3, 4, 5, 18, 7, 8, 9, 6, 11, 12, 13, 10, 15, 16, 17, 14, 19, 23, 20, 21, 22]])
down_ = np.array([[0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 16, 17, 6, 7, 21, 22, 23, 20],
                  [0, 1, 2, 3, 4, 5, 10, 7, 8, 9, 14, 11, 12, 13, 18, 15, 16, 17, 6, 19, 21, 22, 23, 20]])
front = np.array([[0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23],
                  [0, 1, 5, 3, 4, 20, 6, 7, 11, 8, 9, 10, 12, 13, 14, 2, 16, 17, 18, 19, 15, 21, 22, 23]])
front_ = np.array([[0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23],
                   [0, 1, 15, 3, 4, 2, 6, 7, 9, 10, 11, 8, 12, 13, 14, 20, 16, 17, 18, 19, 5, 21, 22, 23]])
back = np.array([[13, 14, 2, 3, 1, 5, 6, 0, 8, 9, 10, 11, 12, 22, 23, 15, 19, 16, 17, 18, 20, 21, 7, 4],
                 [13, 1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 11, 12, 22, 14, 15, 19, 16, 17, 18, 20, 21, 7, 23]])
back_ = np.array([[7, 4, 2, 3, 23, 5, 6, 22, 8, 9, 10, 11, 12, 0, 1, 15, 17, 18, 19, 16, 20, 21, 13, 14],
                  [7, 1, 2, 3, 4, 5, 6, 22, 8, 9, 10, 11, 12, 0, 14, 15, 17, 18, 19, 16, 20, 21, 13, 23]])


# Functions
# Turning the cube
def turn(move, state=solved):
    new = {}
    for x in range(2):
        swaps = move[x]
        pieces = state[x]
        new[x] = []
        for s in swaps:
            new[x].append(pieces[s])
    new_state = np.array([new[0], new[1]])
    return new_state


# Recovers a move
def move(x):
    if x == 'L':
        return left
    elif x == "L'":
        return left_
    elif x == 'R':
        return right
    elif x == "R'":
        return right_
    elif x == 'U':
        return up
    elif x == "U'":
        return up_
    elif x == 'D':
        return down
    elif x == "D'":
        return down_
    elif x == 'F':
        return front
    elif x == "F'":
        return front_
    elif x == 'B':
        return back
    elif x == "B'":
        return back_
    else:
        return print('Invalid Move')


# Converts a string of moves into a list with their individual moves
def qtm(turns):
    X = []
    for i in range(len(turns)):
        a = turns[i]
        if a not in ["'", '2']:
            if turns[(i + 1) % len(turns)] == "'":
                X.append(a + "'")
            elif turns[(i + 1) % len(turns)] == '2':
                X.append(a + '2')
            else:
                X.append(a)
    return X


# Return all unique character strings of a given length
def combo(x, depth=1, cube=True):
    y = x
    while depth != 1:
        z = []
        for a in y:
            for b in x:
                if cube:
                    if len(b) == 1:
                        if a[-1] in ["'", '2'] and b != a[-2]:
                            z.append(a + b)
                        elif a[-1] not in ["'", '2'] and b != a[-1]:
                            z.append(a + b)
                    else:
                        if a[-1] in ["'", '2'] and b[0] != a[-2]:
                            z.append(a + b)
                        elif a[-1] not in ["'", '2'] and b[0] != a[-1]:
                            z.append(a + b)
                else:
                    if b != a[-1]:
                        z.append(a + b)
        y = z
        depth -= 1
        if depth == 1:
            break
    return y


# Calculates the final state for an input scramble
def move_sim(scramble, state=solved):
    s = state
    X = qtm(scramble)
    for x in X:
        if '2' in x:
            for i in range(2):
                m = move(x[0])
                y = turn(m, s)
                s = y
        else:
            m = move(x)
            y = turn(m, s)
            s = y
    return s


# Graphing the Cube
# Colours
colour = ['black', 'orange', 'green', 'red', 'blue', 'yellow']


def colours(n):
    if n in [0, 1, 2, 3]:
        return 'black'
    if n in [4, 5, 6, 7]:
        return 'orange'
    if n in [8, 9, 10, 11]:
        return 'green'
    if n in [12, 13, 14, 15]:
        return 'red'
    if n in [16, 17, 18, 19]:
        return 'blue'
    if n in [20, 21, 22, 23]:
        return 'yellow'


# Coords
def coord(state):
    info = []
    cor = state[0]
    edg = state[1]
    for i in range(24):
        colc = colours(cor[i])
        cole = colours(edg[i])
        # Up
        if i == 0:
            info.append([-3 / 2, 0, 'black'])
            info.append([-4 / 2, -1 / 2, colc])
            info.append([-4 / 2, 0, cole])
        if i == 1:
            info.append([-4 / 2, 1 / 2, colc])
            info.append([-3 / 2, 1 / 2, cole])
        if i == 2:
            info.append([-2 / 2, 1 / 2, colc])
            info.append([-2 / 2, 0, cole])
        if i == 3:
            info.append([-2 / 2, -1 / 2, colc])
            info.append([-3 / 2, -1 / 2, cole])
        # Left
        if i == 4:
            info.append([0, -3 / 2, 'orange'])
            info.append([-1 / 2, -4 / 2, colc])
            info.append([-1 / 2, -3 / 2, cole])
        if i == 5:
            info.append([-1 / 2, -2 / 2, colc])
            info.append([0, -2 / 2, cole])
        if i == 6:
            info.append([1 / 2, -2 / 2, colc])
            info.append([1 / 2, -3 / 2, cole])
        if i == 7:
            info.append([1 / 2, -4 / 2, colc])
            info.append([0, -4 / 2, cole])
        # Front
        if i == 8:
            info.append([0, 0, 'green'])
            info.append([-1 / 2, -1 / 2, colc])
            info.append([-1 / 2, 0, cole])
        if i == 9:
            info.append([-1 / 2, 1 / 2, colc])
            info.append([0, 1 / 2, cole])
        if i == 10:
            info.append([1 / 2, 1 / 2, colc])
            info.append([1 / 2, 0, cole])
        if i == 11:
            info.append([1 / 2, -1 / 2, colc])
            info.append([0, -1 / 2, cole])
        # Right
        if i == 12:
            info.append([0, 3 / 2, 'red'])
            info.append([-1 / 2, 2 / 2, colc])
            info.append([-1 / 2, 3 / 2, cole])
        if i == 13:
            info.append([-1 / 2, 4 / 2, colc])
            info.append([0, 4 / 2, cole])
        if i == 14:
            info.append([1 / 2, 4 / 2, colc])
            info.append([1 / 2, 3 / 2, cole])
        if i == 15:
            info.append([1 / 2, 2 / 2, colc])
            info.append([0, 2 / 2, cole])
        # Back
        if i == 16:
            info.append([6 / 2, 0, 'blue'])
            info.append([7 / 2, 1 / 2, colc])
            info.append([7 / 2, 0, cole])
        if i == 17:
            info.append([7 / 2, -1 / 2, colc])
            info.append([6 / 2, -1 / 2, cole])
        if i == 18:
            info.append([5 / 2, -1 / 2, colc])
            info.append([5 / 2, 0, cole])
        if i == 19:
            info.append([5 / 2, 1 / 2, colc])
            info.append([6 / 2, 1 / 2, cole])
        # Down
        if i == 20:
            info.append([3 / 2, 0, 'yellow'])
            info.append([2 / 2, -1 / 2, colc])
            info.append([2 / 2, 0 / 2, cole])
        if i == 21:
            info.append([2 / 2, 1 / 2, colc])
            info.append([3 / 2, 1 / 2, cole])
        if i == 22:
            info.append([4 / 2, 1 / 2, colc])
            info.append([4 / 2, 0, cole])
        if i == 23:
            info.append([4 / 2, -1 / 2, colc])
            info.append([3 / 2, -1 / 2, cole])
    return info


def viscube(state):
    I = coord(move_sim(state))
    for c in colour:
        X = []
        Y = []
        for i in I:
            if c in i:
                X.append(i[0])
                Y.append(i[1])
        plt.style.use('fivethirtyeight')
        plt.scatter(X, Y, color=c)
    plt.xlabel('Moves:' + state)
    plt.title("Rubik's Cube")
    plt.show()


viscube("FURU'R'F'")

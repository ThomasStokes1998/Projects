import numpy as np
import matplotlib.pyplot as plt


class Cube:
    def __init__(self, colours=("white", "orange", "green", "red", "blue", "yellow")):
        # Solved Cube
        solved = np.array([np.arange(0, 24, 1), np.arange(0, 24, 1)])
        self.solved = solved
        # Generators
        # move[0]=Corners, move[1]=Edges
        self.left = np.array([[18, 1, 2, 17, 7, 4, 5, 6, 0, 9, 10, 3, 12, 13, 14, 15, 16, 23, 20, 19, 8, 21, 22, 11],
                              [0, 1, 2, 17, 7, 4, 5, 6, 8, 9, 10, 3, 12, 13, 14, 15, 16, 23, 18, 19, 20, 21, 22, 11]])
        self.left_ = np.array([[8, 1, 2, 11, 5, 6, 7, 4, 20, 9, 10, 23, 12, 13, 14, 15, 16, 3, 0, 19, 18, 21, 22, 17],
                               [0, 1, 2, 11, 5, 6, 7, 4, 8, 9, 10, 23, 12, 13, 14, 15, 16, 3, 18, 19, 20, 21, 22, 17]])
        self.right = np.array([[0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23],
                               [0, 9, 2, 3, 4, 5, 6, 7, 8, 21, 10, 11, 15, 12, 13, 14, 16, 17, 18, 1, 20, 19, 22, 23]])
        self.right_ = np.array([[0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23],
                                [0, 19, 2, 3, 4, 5, 6, 7, 8, 1, 10, 11, 13, 14, 15, 12, 16, 17, 18, 21, 20, 9, 22, 23]])
        self.up = np.array([[3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23],
                            [3, 0, 1, 2, 8, 5, 6, 7, 12, 9, 10, 11, 16, 13, 14, 15, 4, 17, 18, 19, 20, 21, 22, 23]])
        self.up_ = np.array([[1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23],
                             [1, 2, 3, 0, 16, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 20, 21, 22, 23]])
        self.down = np.array([[0, 1, 2, 3, 4, 5, 18, 19, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 23, 20, 21, 22],
                              [0, 1, 2, 3, 4, 5, 18, 7, 8, 9, 6, 11, 12, 13, 10, 15, 16, 17, 14, 19, 23, 20, 21, 22]])
        self.down_ = np.array([[0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 16, 17, 6, 7, 21, 22, 23, 20],
                               [0, 1, 2, 3, 4, 5, 10, 7, 8, 9, 14, 11, 12, 13, 18, 15, 16, 17, 6, 19, 21, 22, 23, 20]])
        self.front = np.array([[0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23],
                               [0, 1, 5, 3, 4, 20, 6, 7, 11, 8, 9, 10, 12, 13, 14, 2, 16, 17, 18, 19, 15, 21, 22, 23]])
        self.front_ = np.array([[0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23],
                                [0, 1, 15, 3, 4, 2, 6, 7, 9, 10, 11, 8, 12, 13, 14, 20, 16, 17, 18, 19, 5, 21, 22, 23]])
        self.back = np.array([[13, 14, 2, 3, 1, 5, 6, 0, 8, 9, 10, 11, 12, 22, 23, 15, 19, 16, 17, 18, 20, 21, 7, 4],
                              [13, 1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 11, 12, 22, 14, 15, 19, 16, 17, 18, 20, 21, 7, 23]])
        self.back_ = np.array([[7, 4, 2, 3, 23, 5, 6, 22, 8, 9, 10, 11, 12, 0, 1, 15, 17, 18, 19, 16, 20, 21, 13, 14],
                               [7, 1, 2, 3, 4, 5, 6, 22, 8, 9, 10, 11, 12, 0, 14, 15, 17, 18, 19, 16, 20, 21, 13, 23]])
        self.poss_moves = ["U", "U'", "U2", "L", "L'", "L2", "F", "F'", "F2", "R", "R'", "R2", "B", "B'", "B2",
                           "D", "D'", "D2"]
        # Colours
        if len(colours) != 6:
            print("Must name 6 colours")
        else:
            self.colour = colours

    # Functions
    # Turning the cube
    def turn(self, move, state=None, size=2):
        if state is None:
            state = self.solved
        new = {}
        for x in range(size):
            swaps = move[x]
            pieces = state[x]
            new[x] = []
            for s in swaps:
                new[x].append(pieces[s])
        new_state = np.array([new[0], new[1]])
        return new_state

    # Recovers a move
    def move(self, x):
        if x == 'L':
            return self.left
        elif x == "L'":
            return self.left_
        elif x == 'R':
            return self.right
        elif x == "R'":
            return self.right_
        elif x == 'U':
            return self.up
        elif x == "U'":
            return self.up_
        elif x == 'D':
            return self.down
        elif x == "D'":
            return self.down_
        elif x == 'F':
            return self.front
        elif x == "F'":
            return self.front_
        elif x == 'B':
            return self.back
        elif x == "B'":
            return self.back_
        else:
            return print("Invalid Move")

    # Converts a string of moves into a list with their individual moves
    def qtm(self, turns):
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
    def combo(self, x, depth=1, cube=True):
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

    # Generates a scramble of an arbitrary length
    def scramble(self, length=25):
        s = ""
        l = 0
        while l < length:
            n = np.random.randint(0, len(self.poss_moves), 1)[0]
            m = self.poss_moves[n]
            if len(s) == 0:
                s += m
                l += 1
            elif len(m) == 1:
                if s[-1] not in ["'", "2"] and s[-1] != m:  # Ensures successive letters are different
                    if len(s) < 4:
                        s += m
                        l += 1
                    elif s[-2] not in ["'", "2"] and s[-2] != m:  # Ensures no three consecutive letters are the same
                        s += m
                        l += 1
                    elif s[-2] in ["'", "2"] and s[-3] != m:
                        s += m
                        l += 1
                elif s[-1] in ["'", "2"] and s[-2] != m:
                    if s[-3] not in ["'", "2"] and s[-3] != m:
                        s += m
                        l += 1
                    elif s[-3] in ["'", "2"] and s[-4] != m:
                        s += m
                        l += 1
            elif len(m) == 2:
                if s[-1] not in ["'", "2"] and s[-1] != m[0]:  # Ensures successive letters are different
                    if len(s) < 4:
                        s += m
                        l += 1
                    if s[-2] not in ["'", "2"] and s[-2] != m[0]:  # Ensures no three consecutive letters are the same
                        s += m
                        l += 1
                    elif s[-2] in ["'", "2"] and s[-3] != m[0]:
                        s += m
                        l += 1
                elif s[-1] in ["'", "2"] and s[-2] != m[0]:
                    if s[-3] not in ["'", "2"] and s[-3] != m[0]:
                        s += m
                        l += 1
                    elif s[-3] in ["'", "2"] and s[-4] != m[0]:
                        s += m
                        l += 1
        return s

    # Calculates the final state for an input scramble
    def move_sim(self, scramble, state=None):
        if state is None:
            state = self.solved
        s = state
        X = Cube().qtm(scramble)
        for x in X:
            if '2' in x:
                for i in range(2):
                    m = Cube().move(x[0])
                    y = Cube().turn(m, s)
                    s = y
            else:
                m = Cube().move(x)
                y = Cube().turn(m, s)
                s = y
        return s

    # Graphing the Cube
    # Colours
    def colours(self, n):
        if n in [0, 1, 2, 3]:
            return self.colour[0]  # Up
        if n in [4, 5, 6, 7]:
            return self.colour[1]  # Left
        if n in [8, 9, 10, 11]:
            return self.colour[2]  # Front
        if n in [12, 13, 14, 15]:
            return self.colour[3]  # Right
        if n in [16, 17, 18, 19]:
            return self.colour[4]  # Back
        if n in [20, 21, 22, 23]:
            return self.colour[5]  # Down

    # Coords
    def coord(self, state):
        info = []
        cor = state[0]
        edg = state[1]
        for i in range(24):
            colc = Cube().colours(cor[i])
            cole = Cube().colours(edg[i])
            # Up
            if i == 0:
                info.append([-3 / 2, 0, self.colour[0]])
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
                info.append([0, -3 / 2, self.colour[1]])
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
                info.append([0, 0, self.colour[2]])
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
                info.append([0, 3 / 2, self.colour[3]])
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
                info.append([6 / 2, 0, self.colour[4]])
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
                info.append([3 / 2, 0, self.colour[5]])
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

    # Visualises a given sequence of moves
    def viscube(self, state, size=400, style="dark_background"):
        I = Cube().coord(Cube().move_sim(state))
        for c in self.colour:
            X = []
            Y = []
            for i in I:
                if c in i:
                    X.append(i[0])
                    Y.append(i[1])
            plt.style.use(style)
            plt.scatter(X, Y, color=c, linewidths=10, s=size, marker="s")
        plt.xlabel('Moves:' + state)
        plt.title("Rubik's Cube")
        plt.show()


# Test Visualisation
if __name__ == "__main__":
    Cube().viscube(Cube().scramble(25))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

allmovestates = pd.read_csv("optallmoves.csv")
sixmovestates = pd.read_csv("opt6moves.csv")


class Cube2:
    def __init__(self, colours=("white", "orange", "green", "red", "blue", "yellow")):
        self.solved = np.arange(24)
        # Outer layer turns
        self.right = [0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23]
        self.right_ = [0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23]
        self.up = [3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23]
        self.up_ = [1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23]
        self.front = [0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23]
        self.front_ = [0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23]
        # Rotations
        self.eks = [18, 19, 16, 17, 7, 4, 5, 6, 0, 1, 2, 3, 13, 14, 15, 12, 22, 23, 20, 21, 8, 9, 10, 11]
        self.eks_ = [8, 9, 10, 11, 5, 6, 7, 4, 20, 21, 22, 23, 15, 12, 13, 14, 2, 3, 0, 1, 18, 19, 16, 17]
        self.wai = [3, 0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 21, 22, 23, 20]
        self.wai_ = [1, 2, 3, 0, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 23, 20, 21, 22]
        self.zed = [7, 4, 5, 6, 23, 20, 21, 22, 11, 8, 9, 10, 3, 0, 1, 2, 17, 18, 19, 16, 15, 12, 13, 14]
        self.zed_ = [13, 14, 15, 12, 1, 2, 3, 0, 9, 10, 11, 8, 21, 22, 23, 20, 19, 16, 17, 18, 5, 6, 7, 4]
        # Lists
        self.poss_moves = ["U", "U'", "U2", "F", "F'", "F2", "R", "R'", "R2"]
        self.rotations = ["", "x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2", "xy", "xy2", "xy'", "x'y", "x'y'",
                          "x'y2", "x2y", "x2y'", "xz", "xz'", "x'z", "x'z'", "x2z", "x2z'"]
        self.colour = colours
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.amstates = allmovestates.columns
        self.smstates = sixmovestates.columns

    # Functions
    # Turning the cube
    def turn(self, move, state=None):
        if state is None:
            state = self.solved
        swaps = move
        pieces = state
        new = []
        for s in swaps:
            new.append(pieces[s])
        return new

    # Retrieving a move
    def move(self, x: str):
        if x == "U":
            return self.up
        elif x == "U'":
            return self.up_
        elif x == "F":
            return self.front
        elif x == "F'":
            return self.front_
        elif x == "R":
            return self.right
        elif x == "R'":
            return self.right_
        elif x == "x":
            return self.eks
        elif x == "x'":
            return self.eks_
        elif x == "y":
            return self.wai
        elif x == "y'":
            return self.wai_
        elif x == "z":
            return self.zed
        elif x == "z'":
            return self.zed_
        else:
            return print("Invalid move!")

    # Finds all moves up to a given depth
    def moveCombo(self, depth=6):
        if depth == 1:
            return self.poss_moves
        else:
            z = [self.poss_moves]
            for d in range(depth - 1):
                lastmoves = z[d]
                newmoves = []
                for lm in lastmoves:
                    if lm[len(lm) - 1] == "'" or lm[len(lm) - 1] == "2":
                        laststr = lm[len(lm) - 2]
                    else:
                        laststr = lm[len(lm) - 1]
                    for m in self.poss_moves:
                        if m[0] != laststr:
                            newmoves.append(lm + m)
                z.append(newmoves)
        return z

    # Converts a string of moves into a list with their individual moves
    def qtm(self, turns: str):
        X = []
        for i in range(len(turns)):
            a = turns[i]
            # Rotations
            if a in ["x", "y", "z"]:
                if turns[(i + 1) % len(turns)] == "'":
                    X.append(a + "'")
                elif turns[(i + 1) % len(turns)] == '2':
                    X.append(a + '2')
                else:
                    X.append(a)
            elif a not in ["'", '2']:
                if turns[(i + 1) % len(turns)] == "'":
                    X.append(a + "'")
                elif turns[(i + 1) % len(turns)] == '2':
                    X.append(a + '2')
                # Regular Turn
                else:
                    X.append(a)
        return X

    # Returns a scramble of a given length
    def scramble(self, length: int = 12):
        s = ""
        l = 0
        ns = []
        while l < length:
            n = np.random.randint(0, 9, 1)[0]
            m = self.poss_moves[n]
            if l == 0:
                s += m
                ns.append(n)
                l += 1
            elif ns[l - 1] // 3 != n // 3:
                s += m
                ns.append(n)
                l += 1
        return s

    # Encodes a state as a string
    def encodeScramble(self, scramble: str, state=None) -> str:
        if state is None:
            state = self.solved
        nstate = Cube2().move_sim(scramble, state)
        e = ""
        for s in nstate:
            e += self.letters[s]
        return e

    # Inverts a scramble
    def invertScramble(self, scramble: str) -> str:
        inv = ""
        qscramble = Cube2().qtm(scramble)
        for i in range(len(qscramble)):
            s = qscramble[-i - 1]
            if "'" in s:
                inv += s[0]
            elif len(s) == 1:
                inv += s + "'"
            else:
                inv += s
        return inv

    # Finds the optimal solution for a scramble
    def optimalSolution(self, scramble, initstate=None):
        optlength = 12
        optsoln = ""
        uniquemoves = Cube2().moveCombo(5)
        if initstate is None:
            initstate = self.solved
        for rot in ["", "y", "y2", "y'", "x2", "x2y", "x2y2", "x2y'"]:
            # Checks if the scramble can be solved in 6 moves or less
            init_ms = Cube2().move_sim(scramble + rot, initstate)
            init_encode = Cube2().encodeScramble(scramble + rot, initstate)
            if init_encode in self.amstates:
                optmoves = allmovestates[init_encode][0]
                if ";" in optmoves:
                    optmoves = optmoves.split(";")[0]
                l = len(Cube2().qtm(optmoves))
                if l < optlength:
                    optsoln = rot + Cube2().invertScramble(optmoves)
                    optlength = l
            elif optlength > 6:
                for d in range(min(5, optlength - 6)):
                    umoves = uniquemoves[d]
                    for um in umoves:
                        new_encode = Cube2().encodeScramble(um, init_ms)
                        if new_encode in self.smstates:
                            optmoves = sixmovestates[new_encode][0]
                            if ";" in optmoves:
                                optmoves = optmoves.split(";")[0]
                            l = len(Cube2().qtm(um+optmoves))
                            if l < optlength:
                                optsoln = rot + um + Cube2().invertScramble(optmoves)
                                optlength = l
                                break
                    if d > optlength - 7:
                        break
        return optsoln

    # Simulates a given string of moves
    def move_sim(self, scramble: str, state=None):
        if state is None:
            state = self.solved
        s = state
        X = Cube2().qtm(scramble)
        for x in X:
            if '2' in x:
                for i in range(2):
                    m = Cube2().move(x[0])
                    y = Cube2().turn(m, s)
                    s = y
            else:
                m = Cube2().move(x)
                y = Cube2().turn(m, s)
                s = y
        return s

    # Graphing the Cube
    # Colours
    def colours(self, n: int):
        return self.colour[n // 4]

    # Coords
    def coord(self, state):
        info = []
        cor = state

        # Calculates the initial x position
        def f(m):
            if m < 3:
                return m * (3 - m)
            elif m == 3:
                return 2
            elif m == 5:
                return 4

        # Calculates the initial y position
        def g(m):
            if m == 1 or m == 3:
                return 2 * m - 4
            else:
                return 0

        for i in range(24):
            col = Cube2().colours(cor[i])
            n = i // 4
            if n != 4:
                info.append(
                    [-5 / 2 + f(n) + (i - 4 * n) // 2, -1 / 2 + g(n) + ((i - 4 * n) * (4 * n + 3 - i)) / 2, col])
            else:
                m = i % 4
                info.append([9 / 2 - m // 2, 1 / 2 - m * (3 - m) / 2, col])
        return info

    # Visualises a given sequence of moves
    def viscube(self, scramble: str, size: int = 400, style="dark_background"):
        I = Cube2().coord(Cube2().move_sim(scramble))
        for c in self.colour:
            X = []
            Y = []
            for i in I:
                if c in i:
                    X.append(i[0])
                    Y.append(i[1])
            plt.style.use(style)
            plt.scatter(X, Y, color=c, linewidths=10, s=size, marker="s")
        plt.xlabel('Moves:' + scramble)
        plt.title("Rubik's Cube")
        plt.show()


# Test Visualisation
if __name__ == "__main__":
    s = Cube2().scramble()
    print("Scramble: ", s)
    print("Optimal Solution:", Cube2().optimalSolution(s))
    # Cube2().viscube(s)

import random
import math

def factorialDecode(enc, n):
    enc_list = []
    cor_list = [i for i in range(n)]
    for m in reversed(range(n)):
        x, enc = divmod(enc, math.factorial(m))
        enc_list.append(cor_list[x])
        cor_list.remove(cor_list[x])
    return enc_list

def read_heursitics(filename: str) -> list:
    heur = []
    with open(filename, 'rb') as f:
        line = f.read().strip()
        for b in line:
            heur.append(b-0x61)
        return heur
    
optimal_table = read_heursitics("twobytwotable.txt")

class Cube2:
    def __init__(self, colours=("white", "orange", "green", "red", "blue", "yellow")):
        self.movedict = {
            # Outer layer turns
            "":[x for x in range(24)],
            "R":[0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23],
            "R2":[0, 21, 22, 3, 4, 5, 6, 7, 8, 19, 16, 11, 14, 15, 12, 13, 10, 17, 18, 9, 20, 1, 2, 23],
            "R'":[0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23],
            "U":[3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23],
            "U2":[2, 3, 0, 1, 12, 13, 6, 7, 16, 17, 10, 11, 4, 5, 14, 15, 8, 9, 18, 19, 20, 21, 22, 23],
            "U'":[1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23],
            "F":[0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23],
            "F2":[0, 1, 20, 21, 4, 15, 12, 7, 10, 11, 8, 9, 6, 13, 14, 5, 16, 17, 18, 19, 2, 3, 22, 23],
            "F'":[0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23],
            # Rotations
            "x":[18, 19, 16, 17, 7, 4, 5, 6, 0, 1, 2, 3, 13, 14, 15, 12, 22, 23, 20, 21, 8, 9, 10, 11],
            "x2":[20, 21, 22, 23, 6, 7, 4, 5, 18, 19, 16, 17, 14, 15, 12, 13, 10, 11, 8, 9, 0, 1, 2, 3],
            "x'":[8, 9, 10, 11, 5, 6, 7, 4, 20, 21, 22, 23, 15, 12, 13, 14, 2, 3, 0, 1, 18, 19, 16, 17],
            "y":[3, 0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 21, 22, 23, 20],
            "y2":[2, 3, 0, 1, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 20, 21],
            "y'":[1, 2, 3, 0, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 23, 20, 21, 22],
            "z":[7, 4, 5, 6, 23, 20, 21, 22, 11, 8, 9, 10, 3, 0, 1, 2, 17, 18, 19, 16, 15, 12, 13, 14],
            "z2":[22, 23, 20, 21, 14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 18, 19, 16, 17, 2, 3, 0, 1],
            "z'":[13, 14, 15, 12, 1, 2, 3, 0, 9, 10, 11, 8, 21, 22, 23, 20, 19, 16, 17, 18, 5, 6, 7, 4]
        }

        self.poss_moves = ["U", "U'", "U2", "F", "F'", "F2", "R", "R'", "R2"]
        self.rotations = ["", "x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2", "xy", "xy2", "xy'", "x'y", "x'y'",
                          "x'y2", "x2y", "x2y'", "xz", "xz'", "x'z", "x'z'", "x2z", "x2z'"]
        self.colour = colours
        self.cornernames = {"UBL":[0,4,17], "UBR":[1,16,13], "UFR":[2,12,9], "UFL":[3,8,5],
        "DFL":[20,6,11], "DFR":[21,10,15], "DBR":[22,14,19], "DBL":[23,18,7]}
        self.co_positions = [self.cornernames[c][0] for c in self.cornernames]
        self.co_cw_positions = [self.cornernames[c][1] for c in self.cornernames]
        self.cornamesinv = [0,1,2,3,0,3,4,7,3,2,5,4,2,1,6,5,1,0,7,6,4,5,6,7]
        self.cornerorder = [0,4,17,1,16,13,2,12,9,3,8,5,20,6,11,21,10,15,22,14,19,23,18,7]

    # Functions
    # Turning the cube
    def turn(self, move: str, state: list=None) -> list:
        if state is None:
            state = self.movedict[""]
        return [state[m] for m in move]

    # Retrieving a move
    def move(self, x: str) -> list:
        if x in self.movedict:
            return self.movedict[x]
        print(f"Move not in dictionary: {x}")
        # Returns empty move by default
        return self.movedict[""]

     # Converts a string of moves into a list with their individual moves
    
    def htm(self, turns: str) -> list:
        movelist = []
        m = ""
        for t in turns:
            if t == " ":
                continue
            if t in ["'", "2"]:
                    m += t
            else:
                if len(m) > 0:
                    movelist.append(m)
                m = t
        movelist.append(m)
        return movelist

    # Calculates the final state for an input scramble
    def moveSim(self, scramble: str, state: list=None, singlemove: bool = False) -> list:
        if state is None:
            state = self.movedict[""]
        if not singlemove:
            moves = self.htm(scramble)
        else:
            moves = [scramble]
        s = state
        for m in moves:
            m_ = self.move(m)
            s = self.turn(m_,s)
        return s

    # Encodes a state as tuple of two integers representing the orientation and
    # permutation of the pieces
    def encodeState(self, scramble: str=None, state: list=None) -> str:
        if state is None:
            state = self.moveSim(scramble)
        co, cp = 0, 0
        # Orientation (0 - 3^6-1)
        for i, o in enumerate(self.co_positions[:-2]):
            x = state[o]
            if x in self.co_cw_positions:
                co += 3 ** i
            elif x not in self.co_positions:
                co += 2 * 3 ** i
        # Permutation (0 - 7!-1)
        corlist = [i for i in range(7)]
        for i, o in enumerate(self.co_positions[:-1]):
            x = state[o]
            c_ = self.cornamesinv[x]
            # Add corner value
            for j, c in enumerate(corlist):
                if c_ == c:
                    corlist.remove(c)
                    cp += math.factorial(6 - i) * j
                    break
        return co + 3 ** 6 * cp

    def encodeStateInv(self, enc):
        new_state = [i for i in range(24)]
        cp, co = divmod(enc, 3 ** 6)
        perm = factorialDecode(cp, 7)
        ori = []
        for _ in range(6):
            co, x = divmod(co, 3)
            ori.append(x)
        s = sum(ori) % 3
        if s == 0:
            ori.append(0)
        else:
            ori.append(3 - s)
        for i, o in enumerate(ori):
            p = perm[i]
            for j in range(3):
                new_state[self.cornerorder[3 * i + j]] = self.cornerorder[3 * p + ((o + j) % 3)]
        return new_state

    # Inverts a sequence of moves
    def invertMoves(self, moves:str) -> str:
        invmoves = ""
        movelist = self.htm(moves)
        for m in reversed(movelist):
            if len(m) == 1:
                invmoves += m + "'"
            elif "2" in m:
                invmoves += m
            else:
                invmoves += m[0]
        return invmoves

    # Returns the inverse state for a scramble/state
    def invertScramble(self, scramble: str=None, state: list=None) -> list:
        if scramble is not None:
            return self.moveSim(self.invertMoves(scramble))
        invstate = [0] * 24
        for i, j in enumerate(state):
            invstate[j] = i
        return invstate
    
    # Solves a phase but using Korf style heuristics 
    # (i.e. heuristics that are lower bounds but not necessarily exact)

    def solveKorf(self, mindepth:int, scramble:str=None, state:dict=None, 
                  findingdepth: bool=False, finalphase:bool=True, phasemoves:list=None
                  ,phaseheuristic:list=None):
        # finalphase: true, findingdepth: true -> iterate mindepth until found one soln
        # finalphase: true, findingdepth: false -> return one soln at mindepth
        # finalphase: false, findingdepth: true -> iterate mindepth until found all solns at smallest depth
        # finalphase: false, findingdepth: false -> return all solns at mindepth
        state = self.moveSim(scramble, state)
        searchdepth = mindepth
        if phaseheuristic is None:
            phaseheuristic = optimal_table
        if phasemoves is None:
            phasemoves = self.poss_moves
        state_enc = self.encodeState(state=state)
        if finalphase and not findingdepth:
            minmoves = phaseheuristic[state_enc]
            if minmoves > mindepth:
                return None, mindepth
        
        while findingdepth or searchdepth == mindepth:
            all_states = {state_enc}
            depth_moves = [""]
            for d in range(1, searchdepth + 1):
                statecount = 0
                new_moves = []
                for m in depth_moves:
                    statem = self.moveSim(m, state)
                    if d > 2:
                        h = self.htm(m)
                    for n in phasemoves:
                        if d == 2 and m[0] == n[0]:
                            continue
                        elif d > 2 and h[-1][0] == n[0]:
                            continue

                        statemn = self.moveSim(n, statem, True)
                        enc = self.encodeState(state=statemn)
                        minmoves = phaseheuristic[enc]
                        if minmoves == 0:
                            if finalphase:
                                return m+n, d
                            if findingdepth:
                                depth_moves = []
                                findingdepth = False
                                searchdepth = d
                        # Prune states
                        if minmoves + d > searchdepth or enc in all_states:
                            continue
                        all_states.add(enc)
                        statecount += 1
                        new_moves.append(m+n)
                depth_moves = new_moves
                if d == searchdepth:
                    break
            if not findingdepth:
                return depth_moves, searchdepth
            searchdepth += 1
        return None, searchdepth

    def iterateStates(self) -> list:
        move_count = [0] * 3_674_160
        states = [False] * 3_674_160
        moves = [""]
        enc = self.encodeState("")
        move_count[enc] = 0
        states[enc] = True
        globalstatecount = 1
        d = 1
        while d < 10:
            statecount = 0
            new_moves = []
            for m in moves:
                statem = self.moveSim(m)
                h = self.qtm(m)
                for n in self.poss_moves:
                    if d > 1 and n[0] == h[-1][0]:
                        continue
                    statemn = self.moveSim(n, statem, True)
                    enc = self.encodeState(state=statemn)
                    if states[enc]:
                        continue
                    new_moves.append(m+n)
                    states[enc] = True
                    move_count[enc] = d
                    statecount += 1
                    globalstatecount += 1
            moves = new_moves
            print(f"Finished depth {d} | {statecount} | {globalstatecount}")
            d += 1
        remaining_states = []
        for i, s in enumerate(states):
            if not s:
                remaining_states.append(i)
        while globalstatecount < 3_674_160:
            statecount = 0
            next_states = []
            depth_states = []
            for enc in remaining_states:
                state = self.encodeStateInv(enc)
                new_state = True
                for n in self.poss_moves:
                    staten = self.moveSim(n, state, True)
                    enc_ = self.encodeState(state=staten)
                    if states[enc_]:
                        new_state = False
                        depth_states.append(enc)
                        move_count[enc] = d
                        statecount += 1
                        globalstatecount += 1
                        break
                if new_state:
                    next_states.append(enc)
            for e in depth_states:
                states[e] = True
            remaining_states = next_states
            print(f"Finished depth {d} | {statecount} | {globalstatecount}")
            d += 1
        return move_count
    
#import random
import time
import math

def formatTime(t: float, prec: int = 0):
    h = round(t // 3600)
    t_h = t - 3600 * h
    m = round(t_h // 60)
    t_h_m = t_h - 60 * m
    if prec == 0:
        s = round(t_h_m)
    else:
        s = round(t_h_m, prec)
    if m < 10:
        if s < 10:
            return f"{h}:0{m}:0{s}"
        else:
            return f"{h}:0{m}:{s}"
    elif s < 10:
        return f"{h}:{m}:0{s}"
    else:
        return f"{h}:{m}:{s}"
    
def read_heursitics(filename: str) -> list:
    heur = []
    with open(filename, 'rb') as f:
        line = f.read().strip()
        for b in line:
            y, x = divmod(b, 16)
            heur.append(x)
            heur.append(y)
        return heur

# Load Heuristics
#kcph1_eored = read_heursitics("kcph1_eored.txt")
#kcph1_come = read_heursitics("kcph1_come.txt")
#kcph1_eoco = read_heursitics("kcph1_eoco.txt")
#kcph1_eome = read_heursitics("kcph1_eome.txt")

def encodeOrderedPieces(piececoords:tuple, n:int=12, debug:bool=False):
    m = len(piececoords)
    if debug:
        print(f"piececoords = {piececoords}")
    eop = 0
    xi_ = 0 # Previous coordinate
    for i, xi in enumerate(piececoords):
        for j in range(xi-xi_):
            if debug:
                print(f"({i},{j}): nCr({n-1-xi_-j},{m-1-i}) | {math.comb(n-1-xi_-j,m-1-i)}  {eop}")
            eop += math.comb(n-1-xi_-j,m-1-i)
        xi_ = xi + 1
    if debug:
        print(f"eop = {eop}")
    return eop

# Encodes a list of integers from 0 to n-1 as an integer from 0 to n!-1
def factorialEncode(nums: list):
    n = len(nums)
    enc = 0
    numslist = [i for i in range(n)]
    for i, p in enumerate(nums):
        for j, c in enumerate(numslist):
            if p == c:
                enc += math.factorial(n-1-i)*j
                numslist.remove(c)
                break
    return enc

class Cube:
    def __init__(self, colours: tuple=("white", "orange", "green", "red", "blue", "yellow")):
        # Move dictionary
        self.movedict = {
            "":{
                "corners":[x for x in range(24)], "edges":[x for x in range(24)], "centers":[0, 1, 2, 3, 4, 5]
            },
            # Outer Layer Turns
            "L":{
                "corners":[18, 1, 2, 17, 7, 4, 5, 6, 0, 9, 10, 3, 12, 13, 14, 15, 16, 23, 20, 19, 8, 21, 22, 11],
                "edges":[0, 1, 2, 17, 7, 4, 5, 6, 8, 9, 10, 3, 12, 13, 14, 15, 16, 23, 18, 19, 20, 21, 22, 11],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "L'":{
                "corners":[8, 1, 2, 11, 5, 6, 7, 4, 20, 9, 10, 23, 12, 13, 14, 15, 16, 3, 0, 19, 18, 21, 22, 17],
                "edges":[0, 1, 2, 11, 5, 6, 7, 4, 8, 9, 10, 23, 12, 13, 14, 15, 16, 3, 18, 19, 20, 21, 22, 17],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "L2":{
                "corners":[20, 1, 2, 23, 6, 7, 4, 5, 18, 9, 10, 17, 12, 13, 14, 15, 16, 11, 8, 19, 0, 21, 22, 3],
                "edges":[0, 1, 2, 23, 6, 7, 4, 5, 8, 9, 10, 17, 12, 13, 14, 15, 16, 11, 18, 19, 20, 21, 22, 3],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "R":{
                "corners":[0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23],
                "edges":[0, 9, 2, 3, 4, 5, 6, 7, 8, 21, 10, 11, 15, 12, 13, 14, 16, 17, 18, 1, 20, 19, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "R'":{
                "corners":[0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23],
                "edges":[0, 19, 2, 3, 4, 5, 6, 7, 8, 1, 10, 11, 13, 14, 15, 12, 16, 17, 18, 21, 20, 9, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "R2":{
                "corners":[0, 21, 22, 3, 4, 5, 6, 7, 8, 19, 16, 11, 14, 15, 12, 13, 10, 17, 18, 9, 20, 1, 2, 23],
                "edges":[0, 21, 2, 3, 4, 5, 6, 7, 8, 19, 10, 11, 14, 15, 12, 13, 16, 17, 18, 9, 20, 1, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "U":{
                "corners":[3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23],
                "edges":[3, 0, 1, 2, 8, 5, 6, 7, 12, 9, 10, 11, 16, 13, 14, 15, 4, 17, 18, 19, 20, 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "U'":{
                "corners":[1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23],
                "edges":[1, 2, 3, 0, 16, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 20, 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "U2":{
                "corners":[2, 3, 0, 1, 12, 13, 6, 7, 16, 17, 10, 11, 4, 5, 14, 15, 8, 9, 18, 19, 20, 21, 22, 23],
                "edges":[2, 3, 0, 1, 12, 5, 6, 7, 16, 9, 10, 11, 4, 13, 14, 15, 8, 17, 18, 19, 20 , 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "D":{
                "corners":[0, 1, 2, 3, 4, 5, 18, 19, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 23, 20, 21, 22],
                "edges":[0, 1, 2, 3, 4, 5, 18, 7, 8, 9, 6, 11, 12, 13, 10, 15, 16, 17, 14, 19, 23, 20, 21, 22],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "D'":{
                "corners":[0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 16, 17, 6, 7, 21, 22, 23, 20],
                "edges":[0, 1, 2, 3, 4, 5, 10, 7, 8, 9, 14, 11, 12, 13, 18, 15, 16, 17, 6, 19, 21, 22, 23, 20],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "D2":{
                "corners":[0, 1, 2, 3, 4, 5, 14, 15, 8, 9, 18, 19, 12, 13, 6, 7, 16, 17, 10, 11, 22, 23, 20, 21],
                "edges":[0, 1, 2, 3, 4, 5, 14, 7, 8, 9, 18, 11, 12, 13, 6, 15, 16, 17, 10, 19, 22, 23, 20, 21],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "F":{
                "corners":[0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23],
                "edges":[0, 1, 5, 3, 4, 20, 6, 7, 11, 8, 9, 10, 12, 13, 14, 2, 16, 17, 18, 19, 15, 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "F'":{
                "corners":[0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23],
                "edges":[0, 1, 15, 3, 4, 2, 6, 7, 9, 10, 11, 8, 12, 13, 14, 20, 16, 17, 18, 19, 5, 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "F2":{
                "corners":[0, 1, 20, 21, 4, 15, 12, 7, 10, 11, 8, 9, 6, 13, 14, 5, 16, 17, 18, 19, 2, 3, 22, 23],
                "edges":[0, 1, 20, 3, 4, 15, 6, 7, 10, 11, 8, 9, 12, 13, 14, 5, 16, 17, 18, 19, 2, 21, 22, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "B":{
                "corners":[13, 14, 2, 3, 1, 5, 6, 0, 8, 9, 10, 11, 12, 22, 23, 15, 19, 16, 17, 18, 20, 21, 7, 4],
                "edges":[13, 1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 11, 12, 22, 14, 15, 19, 16, 17, 18, 20, 21, 7, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "B'":{
                "corners":[7, 4, 2, 3, 23, 5, 6, 22, 8, 9, 10, 11, 12, 0, 1, 15, 17, 18, 19, 16, 20, 21, 13, 14],
                "edges":[7, 1, 2, 3, 4, 5, 6, 22, 8, 9, 10, 11, 12, 0, 14, 15, 17, 18, 19, 16, 20, 21, 13, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            "B2":{
                "corners":[22, 23, 2, 3, 14, 5, 6, 13, 8, 9, 10, 11, 12, 7, 4, 15, 18, 19, 16, 17, 20, 21, 0, 1],
                "edges":[22, 1, 2, 3, 4, 5, 6, 13, 8, 9, 10, 11, 12, 7, 14, 15, 18, 19, 16, 17, 20, 21, 0, 23],
                "centers":[0, 1, 2, 3, 4, 5]
            },
            # Middle Layer Turns
            "M":{
                "corners":[x for x in range(24)],
                "edges":[18, 1, 16, 3, 4, 5, 6, 7, 0, 9, 2, 11, 12, 13, 14, 15, 22, 17, 20, 19, 8, 21, 10, 23],
                "centers":[4, 1, 0, 3, 5, 2]
            },
            "M'":{
                "corners":[x for x in range(24)],
                "edges":[8, 1, 10, 3, 4, 5, 6, 7, 20, 9, 22, 11, 12, 13, 14, 15, 2, 17, 0, 19, 18, 21, 16, 23],
                "centers":[2, 1, 5, 3, 0, 4]
            },
            "M2":{
                "corners":[x for x in range(24)],
                "edges":[20, 1, 22, 3, 4, 5, 6, 7, 18, 9, 16, 11, 12, 13, 14, 15, 10, 17, 8, 19, 0, 21, 2, 23],
                "centers":[5, 1, 4, 3, 2, 0]
            },
            "E":{
                "corners":[x for x in range(24)],
                "edges":[0, 1, 2, 3, 4, 17, 6, 19, 8, 5, 10, 7, 12, 9, 14, 11, 16, 13, 18, 15, 20, 21, 22, 23],
                "centers":[0, 4, 1, 2, 3, 5]
            },
            "E'":{
                "corners":[x for x in range(24)],
                "edges":[0, 1, 2, 3, 4, 9, 6, 11, 8, 13, 10, 15, 12, 17, 14, 19, 16, 5, 18, 7, 20, 21, 22, 23],
                "centers":[0, 2, 3, 4, 1, 5]
            },
            "E2":{
                "corners":[x for x in range(24)],
                "edges":[0, 1, 2, 3, 4, 13, 6, 15, 8, 17, 10, 19, 12, 5, 14, 7, 16, 9, 18, 11, 20, 21, 22, 23],
                "centers":[0, 3, 4, 1, 2, 5]
            },
            "S":{
                "corners":[x for x in range(24)],
                "edges":[0, 4, 2, 6, 23, 5, 21, 7, 8, 9, 10, 11, 3, 13, 1, 15, 16, 17, 18, 19, 20, 12, 22, 14],
                "centers":[1, 5, 2, 0, 4, 3]
            },
            "S'":{
                "corners":[x for x in range(24)],
                "edges":[0, 14, 2, 12, 1, 5, 3, 7, 8, 9, 10, 11, 21, 13, 23, 15, 16, 17, 18, 19, 20, 6, 22, 4],
                "centers":[3, 0, 2, 5, 4, 1]
            },
            "S2":{
                "corners":[x for x in range(24)],
                "edges":[0, 23, 2, 21, 14, 5, 12, 7, 8, 9, 10, 11, 6, 13, 4, 15, 16, 17, 18, 19, 20, 3, 22, 1],
                "corners":[5, 3, 2, 1, 4, 0]
            },
            # Wide Turns
            "Lw":{
                "corners":[18, 1, 2, 17, 7, 4, 5, 6, 0, 9, 10, 3, 12, 13, 14, 15, 16, 23, 20, 19, 8, 21, 22, 11],
                "edges":[18, 1, 16, 17, 7, 4, 5, 6, 0, 9, 2, 3, 12, 13, 14, 5, 20, 21, 22, 19, 8, 21, 10, 11],
                "centers":[4, 1, 0, 3, 5, 2]
            },
            "Lw'":{
                "corners":[8, 1, 2, 11, 5, 6, 7, 4, 20, 9, 10, 23, 12, 13, 14, 15, 16, 3, 0, 19, 18, 21, 22, 17],
                "edges":[8, 1, 10, 11, 5, 6, 7, 4, 20, 9, 22, 23, 12, 13, 14, 15, 2, 3, 1, 19, 18, 21, 16, 17],
                "centers":[2, 1, 5, 3, 0, 4]
            },
            "Lw2":{
                "corners":[20, 1, 2, 23, 6, 7, 4, 5, 18, 9, 10, 17, 12, 13, 14, 15, 16, 11, 8, 19, 0, 21, 22, 3],
                "edges":[20, 1, 22, 23, 6, 7, 4, 5, 18, 9, 16, 17, 12, 13, 14, 15, 10, 11, 8, 19, 0, 21, 2, 3],
                "centers":[5, 1, 4, 3, 2, 0]
            },
            "Rw":{
                "corners":[0, 9, 10, 3, 4, 5, 6, 7, 8, 21, 22, 11, 15, 12, 13, 14, 2, 17, 18, 1, 20, 19, 16, 23],
                "edges":[8, 9, 10, 3, 4, 5, 6, 7, 20, 21, 22, 11, 15, 12, 13, 14, 2, 17, 0, 1, 18, 19, 16, 23],
                "centers":[2, 1, 5, 3, 0, 4]
            },
            "Rw'":{
                "corners":[0, 19, 16, 3, 4, 5, 6, 7, 8, 1, 2, 11, 13, 14, 15, 12, 22, 17, 18, 21, 20, 9, 10, 23],
                "edges":[18, 19, 16, 3, 4, 5, 6, 7, 0, 1, 2, 11, 13, 14, 15, 12, 20, 17, 22, 23, 8, 9, 10, 23],
                "centers":[4, 1, 0, 3, 5, 2]
            },
            "Rw2":{
                "corners":[0, 21, 22, 3, 4, 5, 6, 7, 8, 19, 16, 11, 14, 15, 12, 13, 10, 17, 18, 9, 20, 1, 2, 23],
                "edges":[20, 21, 22, 3, 4, 5, 6, 7, 18, 19, 16, 11, 14, 15, 12, 13, 10, 17, 8, 9, 0, 1, 2, 23],
                "centers":[5, 1, 4, 3, 2, 0]
            },
            "Uw":{
                "corners":[3, 0, 1, 2, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 4, 5, 18, 19, 20, 21, 22, 23],
                "edges":[3, 0, 1, 2, 8, 9, 6, 11, 12, 13, 10, 15, 16, 17, 14, 19, 4, 5, 18, 7, 20, 21, 22, 23],
                "centers":[0, 2, 3, 4, 1, 5]
            },
            "Uw'":{
                "corners":[1, 2, 3, 0, 16, 17, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 20, 21, 22, 23],
                "edges":[1, 2, 3, 0, 16, 17, 6, 19, 4, 5, 10, 7, 8, 9, 14, 11, 12, 13, 18, 15, 20, 21, 22, 23],
                "centers":[0, 4, 1, 2, 3, 5]
            },
            "Uw2":{
                "corners":[2, 3, 0, 1, 12, 13, 6, 7, 16, 17, 10, 11, 4, 5, 14, 15, 8, 9, 18, 19, 20, 21, 22, 23],
                "edges":[2, 3, 0, 1, 12, 13, 6, 15, 16, 17, 10, 19, 4, 5, 14, 7, 8, 9, 18, 11, 20, 21, 22, 23],
                "centers":[0, 3, 4, 1, 2, 5]
            },
            "Dw":{
                "corners":[0, 1, 2, 3, 4, 5, 18, 19, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 14, 15, 23, 20, 21, 22],
                "edges":[0, 1, 2, 3, 4, 17, 18, 19, 8, 5, 6, 7, 12, 9, 10, 11, 16, 13, 14, 15, 23, 20, 21, 22],
                "centers":[0, 4, 1, 2, 3, 5]
            },
            "Dw'":{
                "corners":[0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 18, 19, 16, 17, 6, 7, 21, 22, 23, 20],
                "edges":[0, 1, 2, 3, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 16, 5, 6, 7, 21, 22, 23, 20],
                "centers":[0, 2, 3, 4, 1, 5]
            },
            "Dw2":{
                "corners":[0, 1, 2, 3, 4, 5, 14, 15, 8, 9, 18, 19, 12, 13, 6, 7, 16, 17, 10, 11, 22, 23, 20, 21],
                "edges":[0, 1, 2, 3, 4, 13, 14, 15, 8, 17, 18, 19, 12, 5, 6, 7, 16, 9, 10, 11, 22, 23, 20, 21],
                "centers":[0, 3, 4, 1, 2, 5]
            },
            "Fw":{
                "corners":[0, 1, 5, 6, 4, 20, 21, 7, 11, 8, 9, 10, 3, 13, 14, 2, 16, 17, 18, 19, 15, 12, 22, 23],
                "edges":[0, 4, 5, 6, 20, 21, 22, 7, 11, 8, 9, 10, 0, 13, 2, 3, 16, 17, 18, 19, 15, 12, 22, 14],
                "centers":[1, 5, 2, 0, 4, 3]
            },
            "Fw'":{
                "corners":[0, 1, 15, 12, 4, 2, 3, 7, 9, 10, 11, 8, 21, 13, 14, 20, 16, 17, 18, 19, 5, 6, 22, 23],
                "edges":[0, 14, 15, 12, 0, 1, 2, 7, 9, 10, 11, 8, 21, 15, 23, 20, 16, 17, 18, 19, 5, 6, 22, 4],
                "centers":[3, 0, 2, 5, 4, 1]
            },
            "Fw2":{
                "corners":[0, 1, 20, 21, 4, 15, 12, 7, 10, 11, 8, 9, 6, 13, 14, 5, 16, 17, 18, 19, 2, 3, 22, 23],
                "edges":[0, 23, 20, 21, 14, 15, 12, 7, 10, 11, 8, 9, 6, 13, 4, 5, 16, 17, 18, 19, 0, 1, 22, 3],
                "centers":[5, 3, 2, 1, 4, 0]
            },
            "Bw":{
                "corners":[13, 14, 2, 3, 1, 5, 6, 0, 8, 9, 10, 11, 12, 22, 23, 15, 19, 16, 17, 18, 20, 21, 7, 4],
                "edges":[13, 14, 2, 12, 0, 5, 2, 3, 8, 9, 10, 11, 21, 22, 23, 15, 19, 16, 17, 18, 20, 6, 7, 4],
                "centers":[3, 0, 2, 5, 4, 1]
            },
            "Bw'":{
                "corners":[7, 4, 2, 3, 23, 5, 6, 22, 8, 9, 10, 11, 12, 0, 1, 15, 17, 18, 19, 16, 20, 21, 13, 14],
                "edges":[7, 4, 2, 6, 20, 5, 22, 23, 8, 9, 10, 11, 0, 1, 2, 15, 17, 18, 19, 16, 20, 12, 13, 14],
                "centers":[1, 5, 2, 0, 4, 3]
            },
            "Bw2":{
                "corners":[22, 23, 2, 3, 14, 5, 6, 13, 8, 9, 10, 11, 12, 7, 4, 15, 18, 19, 16, 17, 20, 21, 0, 1],
                "edges":[22, 23, 2, 21, 14, 5, 12, 13, 8, 9, 10, 11, 6, 7, 4, 15, 18, 19, 16, 17, 20, 3, 0, 1],
                "centers":[5, 3, 2, 1, 4, 0]
            },
            # Rotations
            "x":{
                "corners":[8, 9, 10, 11, 5, 6, 7, 4, 20, 21, 22, 23, 15, 12, 13, 14, 2, 3, 0, 1, 18, 19, 16, 17],
                "edges":[8, 9, 10, 11, 5, 6, 7, 4, 20, 21, 22, 23, 15, 12, 13, 14, 2, 3, 0, 1, 18, 19, 16, 17],
                "centers":[2, 1, 5, 3, 0, 4]
            },
            "x'":{
                "corners":[18, 19, 16, 17, 7, 4, 5, 6, 0, 1, 2, 3, 13, 14, 15, 12, 22, 23, 20, 21, 8, 9, 10, 11],
                "edges":[18, 19, 16, 17, 7, 4, 5, 6, 0, 1, 2, 3, 13, 14, 15, 12, 22, 23, 20, 21, 8, 9, 10, 11],
                "centers":[4, 1, 0, 3, 5, 2]
            },
            "x2":{
                "corners":[20, 21, 22, 23, 6, 7, 4, 5, 18, 19, 16, 17, 14, 15, 12, 13, 10, 11, 8, 9, 0, 1, 2, 3],
                "edges":[20, 21, 22, 23, 6, 7, 4, 5, 18, 19, 16, 17, 14, 15, 12, 13, 10, 11, 8, 9, 0, 1, 2, 3],
                "centers":[5, 1, 4, 3, 2, 0]
            },
            "y":{
                "corners":[3, 0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 21, 22, 23, 20],
                "edges":[3, 0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 21, 22, 23, 20],
                "centers":[0, 2, 3, 4, 1, 5]
            },
            "y'":{
                "corners":[1, 2, 3, 0, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 23, 20, 21, 22],
                "edges":[1, 2, 3, 0, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 23, 20, 21, 22],
                "centers":[0, 4, 1, 2, 3, 5]
            },
            "y2":{
                "corners":[2, 3, 0, 1, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 20, 21],
                "edges":[2, 3, 0, 1, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 20, 21],
                "centers":[0, 3, 4, 1, 2, 5]
            },
            "z":{
                "corners":[7, 4, 5, 6, 23, 20, 21, 22, 11, 8, 9, 10, 3, 0, 1, 2, 17, 18, 19, 16, 15, 12, 13, 14],
                "edges":[7, 4, 5, 6, 23, 20, 21, 22, 11, 8, 9, 10, 3, 0, 1, 2, 17, 18, 19, 16, 15, 12, 13, 14],
                "centers":[1, 5, 2, 0, 4, 3]
            },
            "z'":{
                "corners":[13, 14, 15, 12, 1, 2, 3, 0, 9, 10, 11, 8, 21, 22, 23, 20, 19, 16, 17, 18, 5, 6, 7, 4],
                "edges":[13, 14, 15, 12, 1, 2, 3, 0, 9, 10, 11, 8, 21, 22, 23, 20, 19, 16, 17, 18, 5, 6, 7, 4],
                "centers":[3, 0, 2, 5, 4, 1]
            },
            "z2":{
                "corners":[22, 23, 20, 21, 14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 18, 19, 16, 17, 2, 3, 0, 1],
                "edges":[22, 23, 20, 21, 14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 18, 19, 16, 17, 2, 3, 0, 1],
                "centers":[5, 3, 2, 1, 4, 0]
            }
        }
        # Different Individual Moves and Rotations
        self.poss_moves = ["U", "U'", "U2", "L", "L'", "L2", "F", "F'", "F2", "R", "R'", "R2", "B", "B'", "B2", "D",
                           "D'", "D2", "Uw", "Uw'", "Uw2", "Lw", "Lw'", "Lw2", "Fw", "Fw'", "Fw2", "Rw", "Rw'", "Rw2",
                           "Bw", "Bw'", "Bw2", "Dw", "Dw'", "Dw2", "M", "M'", "M2", "E", "E'", "E2", "S", "S'", "S2"]
        self.rotations = ["", "x", "x'", "x2", "y", "y'", "y2", "z", "z'", "z2", "xy", "xy2", "xy'", "x'y", "x'y'",
                          "x'y2", "x2y", "x2y'", "xz", "xz'", "x'z", "x'z'", "x2z", "x2z'"]
        self.eo_positions = [0, 1, 2, 3, 9, 11, 17, 19, 20, 21, 22, 23]
        self.co_positions = [0, 1, 2, 3, 20, 21, 22, 23]
        self.cw_positions = [4, 16, 12, 8, 6, 10, 14, 18]
        self.edgenames = [0,16,1,12,2,8,3,4,9,15,11,5,17,7,19,13,20,10,21,14,22,18,23,6]
        self.edgenamesinv = [0,1,2,3,3,5,11,6,2,4,8,5,1,7,9,4,0,6,10,7,8,9,10,11]
        self.cornernames = [0,4,17,1,16,13,2,12,9,3,8,5,20,6,11,21,10,15,22,14,19,23,18,7]
        self.cornamesinv = [0,1,2,3,0,3,4,7,3,2,5,4,2,1,6,5,1,0,7,6,4,5,6,7]

        # Colours
        if len(colours) != 6:
            print("Must name exactly 6 colours! Display features will not work!")
        else:
            self.colour = colours

    # Functions
    # Turning the cube
    def turn(self, move: dict, state=None) -> dict:
        if state is None:
            state = self.movedict[""]
        return {piece:[state[piece][m] for m in move[piece]] for piece in state}

    # Recovers a move
    def move(self, x: str) -> dict:
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
            if t in ["'", "2", "w"]:
                    m += t
            else:
                if len(m) > 0:
                    movelist.append(m)
                m = t
        movelist.append(m)
        return movelist

    # Calculates the final state for an input scramble
    def moveSim(self, scramble: str, state: dict=None, singlemove: bool = False):
        if scramble is None:
            return state
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

    # Inverts a sequence of moves
    def invertMoves(self, moves:str) -> str:
        if len(moves) == 0:
            return ""
        invmoves = ""
        movelist = self.htm(moves)
        for m in reversed(movelist):
            if len(m) == 1:
                invmoves += m + "'"
            elif m[1] == "'":
                invmoves += m[0]
            else:
                invmoves += m
        return invmoves

    # Returns the inverse state for a scramble/state
    def invertState(self, state: dict) -> dict:
        invstate = {"corners":[0]*24,"edges":[0]*24,"centers":[0]*6}
        for piece in state:
            for i, j in enumerate(state[piece]):
                invstate[piece][j] = i
        return invstate
        
    # Normalises a state
    def normState(self, scramble:str=None, state:dict=None, rotation:str=None) -> dict:
        if scramble is not None:
            state = self.moveSim(scramble, state)
        if rotation is None:
            for r in self.rotations:
                if self.moveSim(r)["centers"] == state["centers"]:
                    rotation = r
                    break
        rstate = self.moveSim(rotation)
        normr = {piece:{c:i for i,c in enumerate(rstate[piece])} for piece in state}
        return {piece:[normr[piece][x] for x in state[piece]] for piece in state}
    
    # Returns from the default position (white top, green front on a standard Rubik's Cube)
    def normMoves(self, moves: str) -> str:
        outerlayerturns = "ULFRBD"
        moveconversion = {o:o for o in outerlayerturns}
        nmoves = ""
        findingrot = True
        r = ""
        n = ""
        for m in moves:
            if findingrot and m not in outerlayerturns:
                r += m
            elif findingrot:
                rcentres = self.moveSim(r)["centers"]
                moveconversion = {o:outerlayerturns[rcentres[i]] for i, o in enumerate(outerlayerturns)}
                findingrot = False
            if not findingrot and m not in "xyz":
                n += m
            elif not findingrot:
                for x in n:
                    if x in outerlayerturns:
                        nmoves += moveconversion[x]
                    else:
                        nmoves += x
                r += m
                findingrot = True
                n = ""
        if not findingrot:
            for x in n:
                if x in outerlayerturns:
                    nmoves += moveconversion[x]
                else:
                    nmoves += x
        return nmoves
    
    # Encodes a scramble with 
    # corner orientation, edge orientation, corner permutation, edge permutation
    def encodeState(self, scramble: str=None, state: dict=None) -> int:
        state = self.moveSim(scramble, state)
        co, eo, cp, ep = 0, 0, 0, 0
        corper = []
        for i, c in enumerate(self.co_positions[:7]):
            sticker = state["corners"][c]
            name = self.cornamesinv[sticker]
            corper.append(name)
            if sticker == self.co_positions[name]:
                continue
            if sticker == self.cw_positions[name]:
                co += 3 ** i
            else:
                co += 2 * 3 ** i
        cp = factorialEncode(corper)

        edgper = []
        for i, e in enumerate(self.eo_positions[:11]):
            sticker = state["edges"][e]
            name = self.edgenamesinv[sticker]
            edgper.append(name)
            if sticker == self.eo_positions[name]:
                continue
            eo += 2 ** i
        
        ep = factorialEncode(edgper)

        return co + 3 ** 7 * (eo + 2 ** 11 * (cp + ep * 40_320) )

    def encodeKociembaPhase1(self, scramble:str=None,state:list=None) -> int:
        state = self.moveSim(scramble, state)
        co, eo, me = 0, 0, 0
        for i, c in enumerate(self.co_positions[:7]):
            sticker = state["corners"][c]
            name = self.cornamesinv[sticker]
            if sticker == self.co_positions[name]:
                continue
            if sticker == self.cw_positions[name]:
                co += 3 ** i
            else:
                co += 2 * 3 ** i
        mepos = []
        for i, e in enumerate(self.eo_positions[:11]):
            sticker = state["edges"][e]
            name = self.edgenamesinv[sticker]
            if 4 <= name <= 7:
                mepos.append(i)
            if sticker == self.eo_positions[name]:
                continue
            eo += 2 ** i
        if len(mepos) < 4:
            mepos.append(11)
        me = encodeOrderedPieces(mepos, 12)
        return eo + 2 ** 11 * (co + me * 3 ** 7)
    
    def encodeKociembaPhase2(self, scramble:str=None, state:list=None) -> int:
        state = self.moveSim(scramble, state)
        cp, udp, mp, = 0, 0, 0
        return cp, udp, mp

    # Solves a phase but using Korf style heuristics 
    # (i.e. heuristics that are lower bounds but not necessarily exact)
    # Rewrite to work for arbitrary search
    def solveKorf(self, mindepth:int, phaseHeuristic, scramble:str=None, 
                  state:dict=None, findingdepth: bool=False, finalphase:bool=False, 
                  phasemoves: list=None):
        state = self.moveSim(scramble, state)
        searchdepth = mindepth
        if phasemoves is None:
            phasemoves = self.poss_moves[:18]
        state_enc = self.encodeState(state=state)
        if finalphase and not findingdepth:
            minmoves = phaseHeuristic(state)
            if minmoves > mindepth:
                return None, mindepth
        # finalphase: true, findingdepth: true -> iterate searchdepth until found soln
        # finalphase: true, findingdepth: false -> check mindepth for solutions
        # finalphase: false, findingdepth: true -> iterate searchdepth until found solns
        # finalphase: false, findingdepth: false -> return all solns for mindepth
        while findingdepth or searchdepth == mindepth:
            all_states = {state_enc}
            depth_moves = [""]
            #print(f"=== Starting depth {searchdepth} ===")
            for d in range(1, searchdepth + 1):
                statecount = 0
                new_moves = []
                t0 = time.time()
                for i, m in enumerate(depth_moves):
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
                        minmoves = phaseHeuristic(statemn)
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
                    if i % 100_000 == 99_999:
                        dt = time.time() - t0
                        #print(f"Tried {i+1} states and found {len(new_moves)} new states.  {formatTime(dt)}")
                depth_moves = new_moves
                dt = time.time() - t0
                print(f"depth={d}, states={statecount}  {formatTime(dt)}")
                if d == searchdepth:
                    break
            if not findingdepth:
                return depth_moves, searchdepth
            searchdepth += 1
        return None, searchdepth

    #def kcph1eoredHeur(self, state:dict) -> int:
    #    e = self.encodeKociembaPhase1(state=state) // 2 ** 11
    #    return kcph1_eored[e]
    
    #def kcph1Heur(self, state:dict) -> int:
    #    enc = self.encodeKociembaPhase1(state=state)
    #    come, eo = divmod(enc, 2 ** 11)
    #    me, co = divmod(come, 3 ** 7)
    #    return max(kcph1_come[come], kcph1_eoco[eo + 2 ** 11 * co], kcph1_eome[eo + 2 ** 11 * me])

if __name__ == "__main__":
    rc = Cube()
    
    
    
    
    
    
    
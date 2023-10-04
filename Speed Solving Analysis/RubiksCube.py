import random
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
                "edges":[23, 21, 20, 3, 4, 5, 6, 7, 18, 19, 16, 11, 14, 15, 12, 13, 10, 17, 8, 9, 0, 1, 2, 23],
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
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.lettersinv = {l:i for i,l in enumerate(self.letters)}
        self.eo_positions = [0, 1, 2, 3, 9, 11, 17, 19, 20, 21, 22, 23]
        self.co_positions = [0, 1, 2, 3, 20, 21, 22, 23]
        # [oriented, unoriented]
        self.edgenames = {"UB":[0,16], "UR":[1,12], "UF":[2,8], "UL":[3,4], "FR":[9,15], "FL":[11,5],
        "BL":[17,7], "BR":[19,13], "DF":[20,10], "DR":[21,14], "DB":[22,18], "DL":[23,6]}
        self.edgenamesinv = [0,1,2,3,3,5,11,6,2,4,8,5,1,7,9,4,0,6,10,7,8,9,10,11]
        # [oriented, clockwise, anticlockwise]
        self.cornernames = {"UBL":[0,4,17], "UBR":[1,16,13], "UFR":[2,12,9], "UFL":[3,8,5],
        "DFL":[20,6,11], "DFR":[21,10,15], "DBR":[22,14,19], "DBL":[23,18,7]}
        self.co_cw_positions = [self.cornernames[c][1] for c in self.cornernames]
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
    
    # Return the orientation and permutation of the pieces
    def oriPerState(self, scramble:str=None, state:dict=None):
        state = self.moveSim(scramble, state)
        orientation = []
        permutation = []
        for co in self.co_positions:
            c = state["corners"][co]
            if c in self.co_positions:
                orientation.append(0)
            elif c in self.co_cw_positions:
                orientation.append(1)
            else:
                orientation.append(2)
            permutation.append(self.cornamesinv[c])
        for eo in self.eo_positions:
            e = state["edges"][eo]
            if e in self.eo_positions:
                orientation.append(0)
            else:
                orientation.append(1)
            permutation.append(self.edgenamesinv[e])
        return orientation, permutation

     # Generates a random cube state
    def scramble(self, wcamode:bool=False):
        # Orientation
        co, eo = random.randint(0, 3 ** 7 - 1), random.randint(0, 2 ** 11 - 1)
        orientation = []
        while len(orientation) < 7:
            c = co % 3
            orientation.append(c)
            co = (co - c) // 3
        # Ensures the sum of the corner orientations is a multiple of 3
        somod3 = sum(orientation) % 3
        if somod3 == 0:
            orientation.append(0)
        else:
            orientation.append(3 - somod3)
        while len(orientation) < 19:
            e = eo % 2
            orientation.append(e)
            eo = (eo - e) // 2
        # Ensures the sum of the edge orientation is even
        orientation.append(sum(orientation[8:]) % 2)
        # Permutation
        oddparity = True
        while oddparity:
            cp = [i for i in range(8)]
            random.shuffle(cp)
            ep = [i for i in range(8, 20)]
            random.shuffle(ep)
            # Check if it is a valid permutation
            parity = 0
            # Corner Parity
            solved = []
            buffer = cp[0]
            while len(solved) < 8:
                solved.append(buffer)
                buffer = cp[buffer]
                parity += 1
                if buffer in solved:
                    for c in cp:
                        if c not in solved:
                            buffer = c
                            break
            # Edge Parity
            solved = []
            buffer = ep[0]
            while len(solved) < 12:
                solved.append(buffer)
                buffer = ep[buffer-8]
                parity += 1
                if buffer in solved:
                    for c in ep:
                        if c not in solved:
                            buffer = c
                            break
            if parity % 2 == 0:
                oddparity = False
        permutation = cp + ep
        if wcamode:
            state = [permutation, orientation]
            invscr, _ = self.kociemba(state=state)
            return self.invertMoves(invscr)
        return [permutation, orientation]

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

    # Encodes a scramble with 
    # corner orientation, edge orientation, corner permutation, edge permutation
    def encodeState(self, scramble: str=None, state: dict=None) -> tuple:
        orientation, permutation = self.oriPerState(scramble, state)
        co, eo, cp, ep = 0, 0, 0, 0
        # Orientation
        for i, o in enumerate(orientation):
            if i < 7:
                co += o * 3 ** i
            elif 7 < i < 19:
                eo += o * 2 ** (i - 8)
        # Permutation
        clist = [i for i in range(8)]
        elist = [i for i in range(12)]
        for i, p in enumerate(permutation):
            if i < 8:
                for j, c in enumerate(clist):
                    if p == c:
                        cp += math.factorial(7-i)*j
                        clist.remove(c)
                        break
            else:
                for j, c in enumerate(elist):
                    if p == c:
                        ep += math.factorial(19-i)*j
                        elist.remove(c)
                        break
        return co, eo, cp, ep

    # Encodes an ordered tuple of the form (x1,x2,...,xm) where x1<x2<...<xm are elements of Z_n
    # This is function is non-trivial to derive/explain however Kociemba has an explanation
    # for the special case when n=12 and m=4.
    def encodeOrderedPieces(self, piececoords:tuple, n:int=12, debug:bool=False):
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

    def encodeKociembaPhase1(self, scramble:str=None,state:list=None):
        orientation, permutation = self.oriPerState(scramble, state)
        co, eo = 0, 0
        # Orientation
        for i, o in enumerate(orientation):
            if i < 7:
                co += o * 3 ** i
            elif i > 8:
                eo += o * 2 ** (i - 9)
        # 4 Middle edges
        piececoords = []
        for i, p in enumerate(permutation[8:]):
            if 4 <= p <= 7:
                piececoords.append(i)
        me = self.encodeOrderedPieces(piececoords,12)
        return eo, co, me
    
    def encodeKociembaPhase2(self, scramble:str=None, state:list=None):
        _, permutation = self.oriPerState(scramble, state)
        cp, udp, mp, = 0, 0, 0
        clist = [i for i in range(8)]
        udlist = [0, 1, 2, 3, 8, 9, 10, 11]
        mlist = [4, 5, 6, 7]
        for i, p in enumerate(permutation):
            if i < 8:
                for j, c in enumerate(clist):
                    if p == c:
                        cp += math.factorial(7-i)*j
                        clist.remove(c)
                        break
            elif 11 < i < 16:
                for j, c in enumerate(mlist):
                    if p == c:
                        mlist.remove(c)
                        mp += math.factorial(len(mlist))*j
                        break
            else:
                for j, c in enumerate(udlist):
                    if p == c:
                        udlist.remove(c)
                        udp += math.factorial(len(udlist))*j
                        break
        return cp, udp, mp

    def encodeBlock(self, scramble:str=None, state:list=None, corners=[5], edges=[5,8,9,10,11], tupleenc:bool=True):
        cl, el = len(corners), len(edges)
        orientation, permutation = self.oriPerState(scramble, state)
        cornerinv = {c:i for i,c in enumerate(corners)}
        edgeinv = {e:i for i,e in enumerate(edges)}
        co, cp, eo, ep = 0, 0, 0, 0 
        cornerorder = [] # Order the corner appear in the scramble
        cornerpositions = [] # Positions of the corner pieces
        edgeorder = [] # Order the edges appear in the scramble
        edgepositions = [] # Positions of the edge pieces
        for i, p in enumerate(permutation):
            if i < 8 and p in corners:
                co += orientation[i] * 3 ** len(cornerorder)
                cornerorder.append(i)
                cornerpositions.append(cornerinv[p])
            elif  i >= 8 and p in edges:
                eo += orientation[i] * 2 ** len(edgeorder)
                edgeorder.append(i-8)
                edgepositions.append(edgeinv[p])

        permutedcorners = [i for i in range(cl)]
        for i, p in enumerate(cornerpositions):
            for j, c in enumerate(permutedcorners):
                if p == c:
                    permutedcorners.remove(c)
                    cp += math.factorial(cl-1-i)*j
                    break

        cp = self.encodeOrderedPieces(cornerorder, n=8) + math.comb(8, cl) * cp

        permutededges = [i for i in range(el)]
        for i, p in enumerate(edgepositions):
            for j, c in enumerate(permutededges):
                if p == c:
                    permutededges.remove(c)
                    ep += math.factorial(el-1-i)*j
                    break

        ep = self.encodeOrderedPieces(edgeorder, n=12) + math.comb(12, el) * ep
        maxc, maxe = 3 ** cl, 2 ** el
        if len(corners) == 0:
            return eo + maxe * ep
        if tupleenc:
            return co + maxc * cp, eo + maxe * ep
        return co + maxc * eo + maxc * maxe * cp + maxc * maxe * math.comb(8,cl) * math.factorial(cl) * ep

    # Creates a bitmap with specified dimensions
    def createBitMap(self, bitmapdim:tuple) -> list:
        cases = 1
        for e in bitmapdim:
            cases *= e
        bitmap = [False] * cases
        return bitmap

    # Updates a specified value in a bitmap
    # and returns true/false depending on whether it updated the value
    def updateBitMap(self, bitmap:list, enc:tuple, bitmapdim):
        index = 0
        mult = 1
        for i, e in enumerate(enc):
            index += e * mult
            mult *= bitmapdim[i]
        if index > mult:
            print(f"Encoding = {enc}, dim={bitmapdim}")
            print(f"Index = {index}, multiplier = {mult}")
        if not bitmap[index]:
            bitmap[index] = True
            return bitmap, True
        return bitmap, False

    # Updates a dictionary given a new entry
    def updateDict(self, d:int, enc:tuple, states:dict,pruntable:bool=True):
        newenc = False
        allstates_ = states
        for j, e in enumerate(enc):
            if newenc:
                if j == len(enc) - 2:
                    if pruntable:
                        allstates_[e] = {enc[-1]:d}
                    else:
                        allstates_[e] = [enc[-1]]
                    break
                elif j == len(enc) - 1:
                    if pruntable:
                        allstates_[e] = d
                    break
                allstates_[e] = {}
                allstates_ = allstates_[e]
            elif e not in allstates_:
                if j == len(enc) - 1:
                    if pruntable:
                        allstates_[e] = d
                    else:
                        allstates_.append(e)
                    newenc = True
                    break
                allstates_[e] = {}
                allstates_ = allstates_[e]
                newenc = True
            elif j < len(enc) - 1:
                allstates_ = allstates_[e]
        return states, newenc

    def generatePrunTable(self, encodeState, phasemoves:list=None, maxdepth:int=7, printfreq:int=10_000,
    bitmapdim:tuple=None, printinfo:bool=False, symmetries:list=None):
        if phasemoves is None:
            phasemoves = self.poss_moves[:18]
        if symmetries is None:
            symmetries = [""]
        # Generate the states for symmetries
        symetricstates = {s:self.moveSim(s) for s in symmetries}
        if bitmapdim is not None:
            if type(bitmapdim) is int:
                bitmap = [False] * bitmapdim
            else:
                bitmap = self.createBitMap(bitmapdim)
        states = {}
        symmetric_states = {}
        enc = encodeState("")[1:]
        if type(enc) is int:
            if bitmapdim is not None:
                bitmap[enc] = True
            states[enc] = 0
            symmetric_states[enc] = 0
        else:
            if bitmapdim is not None:
                bitmap, _  = self.updateBitMap(bitmap, enc, bitmapdim)
            states_=states
            for i, e in enumerate(enc):
                if i == len(enc) - 2:
                    states_[e] = {enc[-1]:0}
                    break
                states_[e] = {}
                states_ = states_[e]
            states_ = symmetric_states
            for i, e in enumerate(enc):
                if i == len(enc) - 2:
                    states_[e] = {enc[-1]:0}
                    break
                states_[e] = {}
                states_ = states_[e]
        moves = [""]
        d = 1
        while d <= maxdepth and len(moves) > 0:
            newsymstates = 0
            newmoves = []
            t0 = time.time()
            for i, m in enumerate(moves):
                statem = self.moveSim(m)
                if d > 1:
                    h = self.htm(m)
                for n in phasemoves:
                    # One move deep cancellations
                    if d > 1 and n[0] == h[-1][0]:
                        continue
                    # Two move deep cancellations
                    elif d > 2 and n[0] in ["L", "R"] and h[-1][0] in ["L", "R"] and h[-2][0] in ["L", "R"]:
                        continue
                    elif d > 2 and n[0] in ["U", "D"] and h[-1][0] in ["U", "D"] and h[-2][0] in ["U", "D"]:
                        continue
                    elif d > 2 and n[0] in ["F", "B"] and h[-1][0] in ["F", "B"] and h[-2][0] in ["F", "B"]:
                        continue
                    statemn = self.moveSim(n, statem, True)
                    enc = encodeState(state=statemn)[1:]
                    # Check if a state is a duplicate
                    newenc = False
                    if type(enc) is int:
                        if bitmapdim is not None:
                            newenc = not bitmap[enc]
                        elif enc not in states:
                            newenc = True 
                        if newenc:
                            if bitmapdim is not None:
                                bitmap[enc] = True
                            states[enc] = d
                    else:
                        states, newenc = self.updateDict(d, enc, states)
                    if not newenc:
                        continue
                    newmoves.append(m+n)
                    # Check if a state is part of a new coset
                    newsym = True
                    for sym in symmetries:
                        syminv = self.invertMoves(sym)
                        symstate = symetricstates[sym]
                        conjenc = encodeState(m+n+syminv,symstate)[1:]
                        if type(conjenc) is int:
                            if conjenc in symmetric_states:
                                newsym = False
                                break
                        else:
                            sym_state_ = symmetric_states
                            for e in conjenc:
                                if e not in sym_state_:
                                    break
                                sym_state_ = sym_state_[e]
                            if type(sym_state_) is int:
                                newsym = False
                                break
                        if not newsym:
                            break
                    if newsym:
                        #print(f"New Coset: {m+n} Enc={enc}")
                        newsymstates += 1
                        if type(enc) is int:
                            symmetric_states[enc] = d
                        else:
                            symmetric_states, _ = self.updateDict(d, enc, symmetric_states)
                if printinfo and i % printfreq == printfreq - 1:
                    print(f"Searched {i+1} states and found {len(newmoves)} scrambles, {newsymstates} symmetric states. {formatTime(time.time()-t0)}")
            if printinfo:
                print(f"Depth {d}: {len(newmoves)} states, {newsymstates} symmetric states  {formatTime(time.time()-t0)}")
            d += 1
            moves = newmoves
        return states, symmetric_states

    # General function for solving a phase
    def solvePhase(self, encodePhase, phasemoves: list=None, iterphasemoves: list=None, scramble: str=None, state: dict=None, 
    maxdepth: int=None, pruntree: dict=None, maxprundepth: int=6, encodeState=None, finalphase:bool=False, startprintdepth: int=5,
    maxphasesize: int=None, bitmapdim:tuple=None, printinfo:bool=False) -> tuple:
        if scramble is not None:
            state = self.moveSim(scramble, state)
        if encodeState is None:
            encodeState = self.encodeState
        # Most of the time phasemoves and iterphasemoves will be the same list
        if iterphasemoves is None:
            iterphasemoves = phasemoves
        if phasemoves is None:
            phasemoves = self.poss_moves[1:]
        if maxphasesize is None:
            maxphasesize = 2 * maxprundepth - 1
        if maxdepth is None:
            findingmaxdepth = True
        else:
            findingmaxdepth = False
        if finalphase:
            foundsoln = False
        if pruntree is None:
            t0 = time.time()
            print("Started generating pruning tree.")
            pruntree = self.generatePrunTable(encodePhase, iterphasemoves, maxprundepth, 100_000, bitmapdim)
            print(f"Generated pruning tree. {formatTime(time.time()-t0)}")
        if bitmapdim is not None:
            if type(bitmapdim) is int:
                bitmap = [False] * bitmapdim
            else:
                bitmap = self.createBitMap(bitmapdim)
        # Quickly rule out final phase solutions later on in search when the max final phase is small
        enc = encodePhase(state=state)
        if type(enc) is int:
            if enc in pruntree:
                pruntree_ = pruntree[enc]
            else:
                pruntree_ = {}
        else:
            pruntree_ = pruntree
            
            if type(enc) is not tuple:
                if enc in pruntree:
                    pruntree_ = pruntree[enc]
                else:
                    pruntree_ = None
            else:
                for e in enc:
                    if e not in pruntree_:
                        break
                    else:
                        pruntree_ = pruntree_[e]
        if type(pruntree_) is int and pruntree_ == 0:
            return "", 0
        if finalphase and maxdepth is not None and (type(pruntree_) is not int and maxdepth < maxprundepth or type(pruntree_) is int and pruntree_ >= maxdepth):
            return "", maxdepth
        
        p1tree = {0:[""]}
        enc = encodeState(None, state)
        if bitmapdim is not None:
            if type(enc) is int:
                bitmap[enc] = True
            else:
                bitmap, _ = self.updateBitMap(bitmap, enc, bitmapdim)
        else:
            p1states = {}
            p1states_ = p1states
            for i, e in enumerate(enc):
                if i == len(enc) - 2:
                    p1states_[e] = [enc[-1]]
                    break
                p1states_[e] = {}
                p1states_ = p1states_[e]
        d = 1
        t0 = time.time()
        while maxdepth is None or maxdepth >= d:
            p1tree[d] = []
            if printinfo and d >= startprintdepth:
                print(f"Started depth {d} | {len(p1tree[d-1])} {formatTime(time.time()-t0)}")
            for _, m in enumerate(p1tree[d-1]):
                statem = self.moveSim(m, state)
                if d > 1:
                    h = self.htm(m)
                for n in phasemoves:
                    # One move deep cancellations
                    if d > 1 and n[0] == h[-1][0]:
                        continue
                    # Two move deep cancellations
                    elif d > 2 and n[0] in ["L", "R"] and h[-1][0] in ["L", "R"] and h[-2][0] in ["L", "R"]:
                        continue
                    elif d > 2 and n[0] in ["U", "D"] and h[-1][0] in ["U", "D"] and h[-2][0] in ["U", "D"]:
                        continue
                    elif d > 2 and n[0] in ["F", "B"] and h[-1][0] in ["F", "B"] and h[-2][0] in ["F", "B"]:
                        continue
                    s = self.moveSim(n, statem, True)
                    enc = encodePhase(state=s)
                    prunstate = False
                    # Check if the state is in the pruntree
                    if maxdepth is None or maxdepth - d <= maxprundepth:
                        inpruntree = True
                        if type(enc) is int:
                            if enc in pruntree:
                                pruntree_ = pruntree[enc]
                            else:
                                inpruntree = False
                                pruntree_ = None
                        else:
                            pruntree_ = pruntree
                            for e in enc:
                                if e not in pruntree_:
                                    inpruntree = False
                                    break
                                else:
                                    pruntree_ = pruntree_[e]
                        if inpruntree:
                            if type(pruntree_) is not int:
                                print(f"Pruntree_ type = {type(pruntree_)}. Encoding = {enc}, moves ={m+n}")
                                print(f"Pruntree_ = {pruntree_}")
                            if finalphase and pruntree_ == 0:
                                #print(f"enc = {enc}, moves = {m+n}, depth = {pruntree[enc]}")
                                #print(f"wings = {s['wings']}")
                                return m+n, maxdepth
                            if maxdepth is None:
                                maxdepth = pruntree_ + d
                                if finalphase:
                                    fpmoves = m+n
                                    fpenc = enc
                                    foundsoln = True
                                elif printinfo:
                                    print(f"Min depth = {maxdepth} {formatTime(time.time()-t0)}")
                                p1tree[d] = []
                            minlen = pruntree_ + d
                            if minlen > maxdepth:
                                prunstate = True
                            elif (findingmaxdepth or finalphase) and minlen < maxdepth:  
                                if finalphase:
                                    fpmoves = m+n
                                    fpenc = enc
                                    foundsoln = True
                                maxdepth = minlen
                                if printinfo and not finalphase:
                                    print(f"Min depth = {maxdepth} {formatTime(time.time()-t0)}")
                                p1tree[d] = []
                        elif maxdepth is not None and maxdepth - d <= maxprundepth:
                            prunstate = True
                    if not prunstate:
                        enc = encodeState(state=s)
                        # See if the state is a duplicate
                        newenc = False
                        if type(enc) is int:
                            if bitmapdim is not None and not bitmap[enc]:
                                bitmap[enc] = True
                                newenc = True
                            elif bitmapdim is None and enc not in p1states:
                                p1states.append(enc)
                                newenc = True
                        else:
                            p1states, newenc = self.updateDict(d, enc, p1states, False)
                        if newenc:
                            p1tree[d].append(m+n)
            if finalphase and not foundsoln and maxdepth is not None and maxdepth - d <= maxprundepth:
                return "", maxdepth
            if maxdepth is not None and findingmaxdepth:
                findingmaxdepth = False
            if maxdepth is None and d >= maxphasesize - maxprundepth:
                if finalphase:
                    return None, maxdepth
                return [], maxdepth
            d += 1
        if len(p1tree[maxdepth]) == 0:
            print(f"Maxdepth = {maxdepth}")
            if scramble is None:
                print(state)
            else:
                print(scramble)
            md = maxdepth - 1
            while len(p1tree[md]) == 0:
                md -= 1
            print(f"fpenc {fpmoves} = {fpenc} | d={md} | moves = {p1tree[md]}")
            return [], None
        return p1tree[maxdepth], maxdepth

if __name__ == "__main__":
    # Fix Rw2 edges (23 appears twice)
    rc = Cube()
    rc.generatePrunTable(rc.encodeState, None, 10, 100_000, None, True)
    scr = "R' U' F L2 D L U R2 F D F' R' D2 R U2 B2 D2 B2 R' F2 L2 F2 R' U' F"
    
    
    
    
    
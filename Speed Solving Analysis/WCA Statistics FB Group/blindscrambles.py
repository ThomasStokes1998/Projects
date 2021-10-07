import pandas as pd
from RubiksCube import Cube
from blind import blindletters, solvedPieces
from Facebook.scrambles import eventScrambles, cleanScramble
from datetime import datetime

scrambles = pd.read_csv("WCA Database/WCA_export_Scrambles.tsv", delimiter="\t")
print(scrambles.info())
threebld = eventScrambles("333bf")
rc = Cube()
# Importing a save
pseudo = True
index = 15684
# 1: Luckiest scrambles in terms of number of solved pieces
minval1 = 5
if pseudo:
    p1 = pd.read_csv(f"ps_one_{index}.csv")
    comp1 = list(p1["comp1"])
    rtype1 = list(p1["rtype1"])
    glet1 = list(p1["glet1"])
    scrid1 = list(p1["scrid1"])
    sp1 = list(p1["sp1"])
    scr1 = list(p1["scr1"])
else:
    comp1 = []
    rtype1 = []
    glet1 = []
    scrid1 = []
    scr1 = []
    sp1 = []
# 2: Shortest corner, edge and total memo
if pseudo:
    p2 = pd.read_csv(f"ps_two_{index}.csv")
    comp2 = list(p2["comp2"])
    rtype2 = list(p2["rtype2"])
    glet2 = list(p2["glet2"])
    scr2 = list(p2["scr2"])
    maxcor2 = p2["maxval"][0]
    maxedg2 = p2["maxval"][1]
    maxtot2 = p2["maxval"][2]
else:
    comp2 = ["", "", ""]
    rtype2 = ["", "", ""]
    glet2 = ["", "", ""]
    scr2 = ["", "", ""]
    maxcor2 = 8
    maxedg2 = 12
    maxtot2 = 20
# 3: Luckiest group in terms of average memo length
maxval3 = 56
currgroup = ""
if pseudo:
    p3 = pd.read_csv(f"ps_three_{index}.csv")
    comp3 = list(p3["comp3"])
    rtype3 = list(p3["rtype3"])
    glet3 = list(p3["glet3"])
    memolen = list(p3["memolen"])
    scr3 = [[p3.scr30[j], p3.scr31[j], p3.scr32[j]] for j in range(len(p3))]
    ml = 0
    scrs = []
else:
    comp3 = []
    rtype3 = []
    glet3 = []
    memolen = []
    scr3 = []

# Main Loop
u = datetime.now()
l = len(threebld)
first = len(sp1)
third = len(memolen)
print(f"{l - index} scrambles to check.")
for i in range(l):
    if i > index:
        sc = threebld.scramble[i]
        rt = threebld.roundTypeId[i]
        gl = threebld.groupId[i]
        s = cleanScramble(sc)
        sp = solvedPieces(s)
        cm, em = blindletters(s)
        if len(cm+em) < 20:
            # 1: Luckiest scrambles in terms of number of solved pieces
            if sp >= minval1:
                comp1.append(threebld.competitionId[i])
                rtype1.append(rt)
                glet1.append(gl)
                scrid1.append(threebld.scrambleNum[i])
                scr1.append(sc)
                sp1.append(sp)
                first += 1

            # 2: Shortest corner, edge and total memo
            # Shortest corner memo
            if len(cm) < maxcor2:
                comp2[0] = threebld.competitionId[i]
                rtype2[0] = rt
                glet2[0] = gl
                scr2[0] = sc
                maxcor2 = len(cm)

            # Shortest edge memo
            if len(em) < maxedg2:
                comp2[1] = threebld.competitionId[i]
                rtype2[1] = rt
                glet2[1] = gl
                scr2[1] = sc
                maxedg2 = len(em)

            # Shortest total memo
            if len(cm + em) < maxtot2:
                comp2[2] = threebld.competitionId[i]
                rtype2[2] = rt
                glet2[2] = gl
                scr2[2] = sc
                maxtot2 = len(cm + em)

        # 3: Luckiest group in terms of average memo length
        if rt + gl != currgroup:
            if i > 0 and ml <= maxval3 and len(scrs) == 3:
                comp3.append(threebld.competitionId[i])
                rtype3.append(rt)
                glet3.append(gl)
                scr3.append(scrs)
                memolen.append(round(ml / 3, 2))
                third += 1
            ml = 0
            scrs = []
            currgroup = rt + gl
        ml += len(cm + em)
        scrs.append(threebld.scramble[i])

        # Updates
        if i > 0 and i % 392 == 0:
            dt = datetime.now() - u
            h = dt.seconds // 3600
            m = (dt.seconds - h * 3600) // 60
            sec = dt.seconds - h * 3600 - m * 60
            print(f"{i // 392}% Complete. Time Elapsed: {h} hours {m} minutes {sec} seconds.")
        # Saving at 10% intervals
        if i > index and i % 3921 == 0:
            pseudo_one = pd.DataFrame({"comp1": comp1, "rtype1": rtype1, "glet1": glet1, "scrid1": scrid1, "sp1": sp1,
                                       "scr1": scr1})
            pseudo_one.to_csv(f"ps_one_{i}.csv", index=False)
            pseudo_two = pd.DataFrame({"comp2": comp2, "rtype2": rtype2, "glet2": glet2, "scr2": scr2,
                                       "maxval": [maxcor2, maxedg2, maxtot2]})
            pseudo_two.to_csv(f"ps_two_{i}.csv", index=False)
            pseudo_three = pd.DataFrame({"comp3": comp3, "rtype3": rtype3, "glet3": glet3, "memolen": memolen,
                                         "scr30": [z[0] for z in scr3], "scr31": [z[1] for z in scr3],
                                         "scr32": [z[2] for z in scr3]})
            pseudo_three.to_csv(f"ps_three_{i}.csv", index=False)
        # Printing summary of findings
        if i > 0 and i % 4000 == 0:
            dt = datetime.now() - u
            print("=" * 20 + f"{i} Time elapsed {dt.seconds // 60} minutes {i}" + "=" * 20)
            print(f"There have been {first} scrambles found with at least {minval1} solved pieces." +
                  f"\nThe most solved scramble has {max(sp1)} pieces already solved.")
            print(f"The shortest corner memo found is {maxcor2} letters long." +
                  f"\nThe shortest edge memo found is {maxedg2} letters long." +
                  f"\nThe shortest cube memo found is {maxtot2} letters long.")
            print(f"There have been {third} groups found with an average memo length less than 19." +
                  f"\nThe shortest average memo length found is {min(memolen)} letters long.")
            print("=" * 75)

# 1: Luckiest scrambles in terms of number of solved pieces
one = pd.DataFrame(
    {"Competition": comp1, "Round": rtype1, "Group": glet1, "ScrambleNum": scrid1, "Solved Pieces": sp1,
     "Scramble": scr1})
one.sort_values("Solved Pieces").reset_index(drop="index").to_csv("luckiest_3bld_scrambles.csv", index=False)
print(f"The most solved official scramble has {max(sp1)} pieces already solved.")
# Shortest corner memo
print("=" * 75)
print(f"The shortest corner memo from an official scramble is only {maxcor2} letters long.")
print(f"Competition: {comp2[0]}, Round: {rtype2[0]}, Group: {glet2[0]}\nScramble:{scr2[0]}")
# Shortest edge memo
print("=" * 75)
print(f"The shortest edge memo from an official scramble is only {maxedg2} letters long.")
print(f"Competition: {comp2[1]}, Round: {rtype2[1]}, Group: {glet2[1]}\nScramble:{scr2[1]}")
# Shortest total memo
print("=" * 75)
print(f"The shortest memo from an official scramble is only {maxtot2} letters long.")
print(f"Competition: {comp2[2]}, Round: {rtype2[2]}, Group: {glet2[2]}\nScramble:{scr2[2]}")
# 3: Luckiest group in terms of average memo length
three = pd.DataFrame({"Competition": comp3, "Round": rtype3, "Group": glet3, "Average Memo Length": memolen,
                      "Scramble 1": [z[0] for z in scr3], "Scramble 2": [z[1] for z in scr3],
                      "Scramble 3": [z[2] for z in scr3]})
three.sort_values("Average Memo Length").reset_index(drop="index").to_csv("luckiest_3bld_groups.csv", index=False)
print("=" * 75)
print(f"The shortest average memo length for a group at a WCA comp is {min(memolen)} letters long.")

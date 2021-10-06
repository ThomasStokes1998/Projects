import pandas as pd
from RubiksCube import Cube
from blind import blindletters, solvedPieces
from Facebook.scrambles import eventScrambles, cleanScramble
from datetime import datetime

# Script Goals:
# 1: Luckiest scrambles in terms of number of solved pieces
# Min 5 solved pieces
# Columns: Comp, Round, Group, ScrID, Scramble, SP
# 2: Shortest corner, edge and total memo
# print comp, round, group, scrid for shortest corner, edge and total memo
# 3: Luckiest group in terms of average memo length
# Min avg length = 19
# Columns: Comp, Round, Group, Avg Memo Length, Scr 1, Scr 2, Scr 3

scrambles = pd.read_csv("WCA Database/WCA_export_Scrambles.tsv", delimiter="\t")
print(scrambles.info())
threebld = eventScrambles("333bf")
rc = Cube()

# 1: Luckiest scrambles in terms of number of solved pieces
minval1 = 5
comp1 = []
rtype1 = []
glet1 = []
scrid1 = []
scr1 = []
sp1 = []
# 2: Shortest corner, edge and total memo
comp2 = ["", "", ""]
rtype2 = ["", "", ""]
glet2 = ["", "", ""]
scr2 = ["", "", ""]
maxcor2 = 8
maxedg2 = 12
maxtot2 = 20
# 3: Luckiest group in terms of average memo length
maxval3 = 56
comp3 = []
rtype3 = []
glet3 = []
memolen = []
scr3 = []
currgroup = ""
u = datetime.now()
l = len(threebld)
first = 0
third = 0
print(f"{l} scrambles to check.")
for i in range(l):
    sc = threebld.scramble[i]
    s = cleanScramble(sc)
    sp = solvedPieces(s)
    cm, em = blindletters(s)
    # 1: Luckiest scrambles in terms of number of solved pieces
    if sp >= minval1:
        comp1.append(threebld.competitionId[i])
        rtype1.append(threebld.roundTypeId[i])
        glet1.append(threebld.groupId[i])
        scrid1.append(threebld.scrambleNum[i])
        scr1.append(sc)
        sp1.append(sp)
        first += 1

    # 2: Shortest corner, edge and total memo
    # Shortest corner memo
    if len(cm) < maxcor2:
        comp2[0] = threebld.competitionId[i]
        rtype2[0] = threebld.roundTypeId[i]
        glet2[0] = threebld.groupId[i]
        scr2[0] = sc
        maxcor2 = len(cm)

    # Shortest edge memo
    if len(em) < maxedg2:
        comp2[1] = threebld.competitionId[i]
        rtype2[1] = threebld.roundTypeId[i]
        glet2[1] = threebld.groupId[i]
        scr2[1] = sc
        maxedg2 = len(em)

    # Shortest total memo
    if len(cm + em) < maxtot2:
        comp2[2] = threebld.competitionId[i]
        rtype2[2] = threebld.roundTypeId[i]
        glet2[2] = threebld.groupId[i]
        scr2[2] = sc
        maxtot2 = len(cm + em)

    # 3: Luckiest group in terms of average memo length
    rt = threebld.roundTypeId[i]
    gl = threebld.groupId[i]
    if rt + gl != currgroup:
        if i > 0 and ml <= maxval3 and len(scrs) == 3:
            comp3.append(threebld.competitionId[i])
            rtype3.append(threebld.roundTypeId[i])
            glet3.append(threebld.groupId[i])
            scr3.append(scrs)
            memolen.append(round(ml / 3, 2))
            third += 1
        ml = 0
        scrs = []
        currgroup = rt + gl
    ml += len(cm + em)
    scrs.append(threebld.scramble[i])

    # Updates
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

# 1: Luckiest scrambles in terms of number of solved pieces
one = pd.DataFrame({"Competition": comp1, "Round": rtype1, "Group": glet1, "ScrambleNum": scrid1, "Solved Pieces": sp1,
                    "Scramble": scr1})
one.sort_values("Solved Pieces").reset_index(drop="index").to_csv("luckiest_3bld_scrambles.csv", index=False)
print(f"The most solved official scramble has {max(sp1)} pieces already solved.")
# Shortest corner memo
print("=" * 50)
print(f"The shortest corner memo from an official scramble is only {maxcor2} letters long.")
print(f"Competition: {comp2[0]}, Round: {rtype2[0]}, Group: {glet2[0]}\nScramble:{scr2[0]}")
# Shortest edge memo
print("=" * 50)
print(f"The shortest edge memo from an official scramble is only {maxedg2} letters long.")
print(f"Competition: {comp2[1]}, Round: {rtype2[1]}, Group: {glet2[1]}\nScramble:{scr2[1]}")
# Shortest total memo
print("=" * 50)
print(f"The shortest memo from an official scramble is only {maxtot2} letters long.")
print(f"Competition: {comp2[2]}, Round: {rtype2[2]}, Group: {glet2[2]}\nScramble:{scr2[2]}")
# 3: Luckiest group in terms of average memo length
three = pd.DataFrame({"Competition": comp3, "Round": rtype3, "Group": glet3, "Average Memo Length": memolen,
                      "Scramble 1": [z[0] for z in scr3], "Scramble 2": [z[1] for z in scr3],
                      "Scramble 3": [z[2] for z in scr3]})
three.sort_values("Average Memo Length").reset_index(drop="index").to_csv("luckiest_3bld_groups.csv", index=False)
print(f"The shortest average memo length for a group at a WCA comp is {min(memolen)} letters long.")

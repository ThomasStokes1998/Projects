import pandas as pd
from RubiksCube import Cube
from datetime import datetime
from blind import edge_pieces

scrambles = pd.read_csv("WCA Database/WCA_export_Scrambles.tsv", delimiter="\t")
# print(scrambles.info())

rc = Cube()
pieces = rc.poss_moves[:18]


def eventScrambles(event):
    return scrambles[scrambles.eventId == event].reset_index(drop="index")


def cleanScramble(scr: str) -> str:
    s = ""
    for i in range(len(scr)):
        if scr[i] != " ":
            s += scr[i]
    return s


def crossSolved(scr: str) -> bool:
    edges = rc.move_sim(scr)[1]
    for i in range(6):
        sbool = True
        for j in range(4):
            if edges[4 * i + j] != 4 * i + j:
                sbool = False
                break
        if sbool:
            return True
    return False


def oneMoveCross(scr: str) -> bool:
    edges = rc.move_sim(scr)[1]
    for i in range(6):
        # If two edge colours are not matched then not solvable in one move
        # Saving the unsolved piece for later
        wrclist = []
        wrong_colour = 0
        solved = 0
        for j in range(4):
            e = edges[4 * i + j]
            if e // 4 != i:
                wrong_colour += 1
                wrclist.append(4 * i + j)
            elif e == 4 * i + j:
                solved += 1
            if wrong_colour >= 2:
                break
        # Checks if adjusting the cross layer solves the cross
        if solved == 0 and wrong_colour == 0:
            sbool = False
            for k in range(3):
                p = pieces[3 * i + k]
                pedges = rc.move_sim(scr + p)[1]
                for l in range(4):
                    if pedges[4 * i + l] == 4 * i + l:
                        sbool = True
                    else:
                        sbool = False
                        break
                if sbool:
                    return True
        # Checks if turning face of unsolved piece solves the cross
        elif solved == 3:
            wrc = wrclist[0]
            for ed in edge_pieces:
                if wrc == ed[0]:
                    face = ed[1] // 4
                    break
                elif wrc == ed[1]:
                    face = ed[0] // 4
                    break
            for k in range(3):
                q = pieces[3 * face + k]
                qedges = rc.move_sim(scr + q)[1]
                if qedges[wrc] == wrc:
                    return True
    return False

events = ["333oh", "333"]
index = 10_000
save = True
if save:
    omc = pd.read_csv(f"one_move_cross{index}.csv")
    compid = list(omc["Competition"])
    eventid = list(omc["Event"])
    rtypeid = list(omc["Round"])
    groupid = list(omc["Group"])
    snum = list(omc["Scramble Num"])
    scrid = list(omc["Scramble"])
else:
    index = 0
    compid = []
    eventid = []
    rtypeid = []
    groupid = []
    snum = []
    scrid = []
interval = 10 ** 4
u = datetime.now()
if __name__ == "__main__":
    for event in events:
        df = eventScrambles(event)
        scr = df.scramble
        l = len(scr)
        print("Started " + event)
        print("Scrambles to check:", l - index)
        for i in range(l):
            if i > index:
                scri = scr[i]
                s = cleanScramble(scri)
                if oneMoveCross(s):
                    compid.append(df.competitionId[i])
                    eventid.append(event)
                    rtypeid.append(df.roundTypeId[i])
                    groupid.append(df.groupId[i])
                    scrid.append(scri)
                    snum.append(df.scrambleNum[i])
            if i > index and i % interval == 0:
                t = datetime.now()
                dt = t - u
                hours = dt.seconds // 3600
                minutes = (dt.seconds - hours * 3600) // 60
                print(f"{round(100 * i / l, 2)}% complete. Time Elapsed: {hours} hours {minutes} minutes "
                      f"{dt.seconds - hours * 3600 - minutes * 60} seconds.")
                print(f"Found {len(compid)} official {event} scrambles whose crosses can be solved in one move.")
            if i > index and i % 50_000 == 0:
                c = pd.DataFrame({"Competition": compid, "Event": eventid, "Round": rtypeid, "Group": groupid,
                                  "Scramble Num": snum, "Scramble": scrid})
                c.to_csv(f"one_move_cross{i}.csv", index=False)
        cr = pd.DataFrame({"Competition": compid, "Event": eventid, "Round": rtypeid, "Group": groupid,
                           "Scramble Num": snum, "Scramble": scrid})
        cr.to_csv("OneMoveCrosses " + event + ".csv", index=False)

    crosses = pd.DataFrame(
        {"Competition": compid, "Event": eventid, "Round": rtypeid, "Group": groupid,
         "Scramble Num": snum, "Scramble": scrid})
    if len(crosses) > 0:
        crosses.to_csv("solvedcrosses.csv", index=False)
    else:
        print("There has never been a solved cross in an official scramble.")

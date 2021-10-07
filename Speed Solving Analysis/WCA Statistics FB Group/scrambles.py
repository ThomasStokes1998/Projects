import pandas as pd
from RubiksCube import Cube
from datetime import datetime

scrambles = pd.read_csv("WCA Database/WCA_export_Scrambles.tsv", delimiter="\t")
#print(scrambles.info())

rc = Cube()


def eventScrambles(event):
    return scrambles[scrambles.eventId == event].reset_index(drop="index")


def cleanScramble(scr) -> str:
    s = ""
    for i in range(len(scr)):
        if scr[i] != " ":
            s += scr[i]
    return s


def crossSolved(scr) -> bool:
    edges = rc.move_sim(scr)[1]
    for i in range(6):
        sbool = True
        for j in range(4):
            if edges[4 * i + j] != 4 * i + j:
                e = edges[4 * i + j] // 4
                sbool = False
                break
        if sbool:
            return True
    return False

events = ["333oh", "333"]
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
        print("Started " + event)
        df = eventScrambles(event)
        scr = df.scramble
        l = len(scr)
        print("Scrambles to check:", l)
        for i in range(l):
            s = cleanScramble(scr[i])
            if crossSolved(s):
                compid.append(df.competitionId[i])
                eventid.append(event)
                rtypeid.append(df.roundTypeId[i])
                groupid.append(df.groupId[i])
                scrid.append(scr[i])
                snum.append(df.scrambleNum[i])
            if i > 0 and i % interval == 0:
                t = datetime.now()
                dt = t - u
                v = dt.seconds + (dt.microseconds / 10 ** 6)
                speed = interval / v
                print(f"Speed = {round(speed, 1)} scrambles/second.")
                print(f"Estimated time remaining = {round((l - i) / speed, 3)} seconds")
                print(f"There are {len(compid)} solved crosses found so far.")
                u = datetime.now()
        cr = pd.DataFrame({"Competition": compid, "Event": eventid, "Round": rtypeid, "Group": groupid, "Scramble": scrid})
        cr.to_csv("SolvedCrosses "+event+".csv",index=False)

    crosses = pd.DataFrame({"Competition": compid, "Event": eventid, "Round": rtypeid, "Group": groupid, "Scramble": scrid})
    if len(crosses) > 0:
        crosses.to_csv("solvedcrosses.csv", index=False)
    else:
        print("There has never been a solved cross in an official scramble.")

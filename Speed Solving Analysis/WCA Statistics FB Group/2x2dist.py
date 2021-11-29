import pandas as pd
import time
from datetime import datetime
from RubiksCube2 import Cube2

# The frequency of 2x2 scrambles by optimal solution length by delegate,
# also rankings of top 10 in terms of 4 move 2x2 solutions sorted by count of solutions descending.
# 222 Dist: μ = 8.759, σ = 0.883 skew = -0.836

# results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
scrambles = pd.read_csv('WCA Database/WCA_export_Scrambles.tsv', delimiter='\t')
# persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

twos = scrambles[scrambles.eventId == "222"].reset_index(drop="index")
rc = Cube2()


def getDelegate(comp):
    x = competitions[competitions.id == comp].reset_index(drop="index").wcaDelegate[0]
    delegates = x.split("[{")
    gd = []
    for d in delegates:
        if d != "":
            y = d.split("}")[0]
            gd.append(y)
    return gd


imported = True
lastcount = 4500 # This took a while to do so I made saves every 100 competitions (~30mins)
if imported:
    print("Started importing last save")
    delegate_222 = {}
    delegate_scrs = {}
    imp = pd.read_csv(f"delegate_222 {lastcount}.csv")
    dgs = imp["Delegate"]
    for i in range(len(imp)):
        d = dgs[i]
        delegate_scrs[d] = imp["Scrambles"][i]
        delegate_222[d] = [0] * 8
        for j in range(8):
            delegate_222[d][j] += imp[f"{j + 4}moves"][i]
else:
    delegate_222 = {}
    delegate_scrs = {}
u = datetime.now()
tcs = twos.competitionId.unique()
print(f"{twos.competitionId.nunique() - lastcount} competitions to check.")
count = 0
for comp in tcs:
    count += 1
    if count > lastcount:
        if count % 10 == 1:
            v = time.perf_counter()
        dgs = getDelegate(comp)
        tc = twos[twos.competitionId == comp].reset_index(drop="index")
        l = len(tc)
        for d in dgs:
            if d not in delegate_scrs:
                delegate_scrs[d] = l
                delegate_222[d] = [0] * 8
            else:
                delegate_scrs[d] += l
        for i in range(l):
            s = rc.cleanScramble(tc.scramble[i])
            _, o = rc.optimalSolution(s, info=True, ftrack=True)
            for d in dgs:
                delegate_222[d][o - 4] += 1
        if count % 10 == 0:
            print(f"Last competition entered: {comp} ({count}).")
            print(f"Time Elapsed for last 10 comps: {round(time.perf_counter() - v, 3)} seconds.")
            dt = datetime.now() - u
            dts = dt.seconds
            mn = (dts - dts // 3600 * 3600) // 60
            sec = dts - mn * 60 - dts // 3600 * 3600
            if mn < 10:
                if sec < 10:
                    print(f"Total Time Elapsed for {count - lastcount} comps: 0{dts // 3600}:0{mn}:0{sec}")
                else:
                    print(f"Total Time Elapsed for {count - lastcount} comps: 0{dts // 3600}:0{mn}:{sec}")
            else:
                if sec < 10:
                    print(f"Total Time Elapsed for {count - lastcount} comps: 0{dts // 3600}:{mn}:0{sec}")
                else:
                    print(f"Total Time Elapsed for {count - lastcount} comps: 0{dts // 3600}:{mn}:{sec}")

        if count % 100 == 0:
            dgs = []
            c = {}
            groups = []
            evalue = []
            for i in range(8):
                c[f"{i + 4}moves"] = []
            for d in delegate_scrs:
                dgs.append(d)
                y = delegate_scrs[d]
                groups.append(y)
                x = delegate_222[d]
                s = sum(x)
                m = 0
                for i in range(8):
                    m += x[i] * (i + 4)
                    c[f"{i + 4}moves"].append(x[i])
                if s == 0:
                    evalue.append(0)
                else:
                    evalue.append(round(m / s, 2))
            df = pd.DataFrame({"Delegate": dgs, "Scrambles": groups, "E[Moves]": evalue})
            for i in range(8):
                df[f"{i + 4}moves"] = c[f"{i + 4}moves"]
            df.sort_values("Scrambles", ascending=False).to_csv(f"delegate_222 {count}.csv", index=False)
# Dataframe
dgs = []
c = {}
wc = {}
groups = []
evalue = []
for i in range(8):
    c[f"{i + 4}moves"] = []
    wc[f"{i + 4}moves"] = []
for d in delegate_scrs:
    dgs.append(d)
    y = delegate_scrs[d]
    groups.append(y)
    x = delegate_222[d]
    if d == "Calvin Nielson":
        print(f"{d}'s distribution: {x}")
    s = sum(x)
    m = 0
    if s == 0:
        for i in range(8):
            c[f"{i + 4}moves"].append(0)
            wc[f"{i + 4}moves"].append(0)
        evalue.append(0)
    else:
        for i in range(8):
            m += x[i] * (i + 4)
            c[f"{i + 4}moves"].append(x[i])
            wc[f"{i + 4}moves"].append(round(100 * x[i] / s, 2))
        evalue.append(round(m / s, 2))
df = pd.DataFrame({"Delegate": dgs, "Scrambles": groups, "E[Moves]": evalue})
for i in range(8):
    df[f"{i + 4} moves"] = c[f"{i + 4}moves"]
df.sort_values("4 moves", ascending=False).to_csv(f"2x2DistByDelegate.csv", index=False)
print(
    df.sort_values("4 moves", ascending=False).head(10).reset_index(drop="index")[["Delegate", "Scrambles", "4 moves"]])
for i in range(8):
    df[f"{i + 4} moves%"] = wc[f"{i + 4}moves"]
    df = df.drop([f"{i + 4} moves"], axis=1)
df.sort_values("4 moves%", ascending=False).to_csv(f"2x2DistByDelegateWeighted.csv", index=False)
print("=" * 20 + " Weighted (%) " + "=" * 20)
print(df.sort_values("4 moves%", ascending=False).head(10).reset_index(drop="index")[
          ["Delegate", "Scrambles", "4 moves%"]])

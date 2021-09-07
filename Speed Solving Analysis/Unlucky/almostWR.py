import pandas as pd
from datetime import datetime
import numpy as np

# What I would like is have a table with the number of times a competitor
# is one solve from breaking the event WR average.

low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

# Sorting the competition dataframe in order of when the competition happened
print("Started sorting competition dataframe")
u = datetime.now()
datecodes = []

for i in range(len(competitions)):
    y = competitions.year[i]
    m = competitions.month[i]
    d = competitions.day[i]
    datecodes.append(y * 10 ** 4 + m * 10 ** 2 + d)

competitions["date"] = datecodes
competitions = competitions.sort_values("date").reset_index(drop="index")
t = datetime.now()
dt = t - u
print(f"Competitions dataframe sorted in {dt.microseconds / 1000} milliseconds.")

# Functions
three = results[results.eventId == "333"].reset_index(drop="index")


def res(comp, bestmax, data=three):
    eve = data[data.competitionId == comp].reset_index(drop="index")
    eve = eve[eve.average > 0].reset_index(drop="index")
    return eve[eve.best < bestmax].reset_index(drop="index")


def wcaname(ids):
    z = []
    for wcaid in ids:
        x = persons[persons.id == wcaid].reset_index(drop="index").name
        if len(x) == 0:
            print(wcaid)
            z.append(wcaid)
        else:
            z.append(x[len(x) - 1])
    return z


def wcacountry(ids):
    z = []
    for wcaid in ids:
        x = persons[persons.id == wcaid].reset_index(drop="index").countryId
        if len(x) == 0:
            z.append("Null")
        else:
            z.append(x[len(x) - 1])
    return z


def getCompdate(comps):
    z = []
    for comp in comps:
        x = competitions[competitions.id == comp].reset_index(drop="index").date[0]
        z.append(x)
    return z


def getWRs(event="333"):
    eve = results[results.eventId == event].reset_index(drop="index")
    evewr = eve[eve.regionalAverageRecord == "WR"].reset_index(drop="index")
    evewr["date"] = getCompdate(evewr.competitionId)
    return evewr.sort_values("date").reset_index(drop="index")[["personId", "competitionId", "eventId", "average"]]


# Main loop
debug = False
event = "skewb"
data = results[results.eventId == event].reset_index(drop="index")
eventcomps = data.competitionId.unique()
wravg = getWRs(event).average[0]
main_dict = {}

# Detailed list
wcaids = []
komp = []
v1 = []
v2 = []
v3 = []
v4 = []
bpa = []
cwr = []
mint = []

competitions = competitions[competitions.cancelled == 0].reset_index(drop="index")
comps = competitions.id.unique()
u = datetime.now()
count = 0
print("Started Loop")
for comp in comps:
    count += 1
    if comp in eventcomps:
        df = res(comp, wravg, data)
        l = len(df)
        if l > 0:
            for i in range(l):
                if df.average[i] < wravg:
                    wravg = df.average[i]
                else:
                    a = df["value1"][i]
                    b = df["value2"][i]
                    c = df["value3"][i]
                    d = df["value4"][i]
                    # If there is a DNF in the average
                    if np.min([a, b, c, d]) < 0 and a + b + c + d - np.min([a, b, c, d]) < 3 * wravg:
                        wcaid = df.personId[i]
                        # First DF
                        if wcaid not in main_dict.keys():
                            main_dict[wcaid] = 1
                        else:
                            main_dict[wcaid] += 1

                        # Second DF
                        wcaids.append(wcaid)
                        komp.append(comp)
                        v1.append(a / 100)
                        v2.append(b / 100)
                        v3.append(c / 100)
                        v4.append(d / 100)
                        bpa.append(round((a + b + c + d - np.min([a, b, c, d])) / 300, 2))
                        cwr.append(wravg / 100)

                        x = np.percentile([a, b, c, d], 200 / 3)
                        y = np.max([a, b, c, d])
                        t = 3 * wravg - x - y
                        mint.append(t / 100)

                    # If there are no DNFs in the average
                    elif np.min([a, b, c, d]) > 0 and a + b + c + d - np.max([a, b, c, d]) < 3 * wravg:
                        wcaid = df.personId[i]
                        # First DF
                        if wcaid not in main_dict.keys():
                            main_dict[wcaid] = 1
                        else:
                            main_dict[wcaid] += 1

                        # Second DF
                        wcaids.append(wcaid)
                        komp.append(comp)
                        v1.append(a / 100)
                        v2.append(b / 100)
                        v3.append(c / 100)
                        v4.append(d / 100)
                        bpa.append(round((a + b + c + d - np.max([a, b, c, d])) / 300, 2))
                        cwr.append(wravg / 100)

                        x = np.percentile([a, b, c, d], 100 / 3)
                        y = np.percentile([a, b, c, d], 200 / 3)
                        t = 3 * wravg - x - y
                        mint.append(t / 100)

    if count % 100 == 0:
        dt = datetime.now() - u
        print(f"Time elapsed for {count} competitions: {dt}")
    if debug and count % 1000 == 0:
        personId = list(main_dict.keys())
        misses = []
        for i in range(len(personId)):
            misses.append(main_dict[personId[i]])
        s = pd.DataFrame({"Name": personId, "Missed Chances": misses})
        s.to_csv(f"unlucky {event} {count}.csv", index=False)

print("Total elapsed time :", datetime.now() - u)
# First dataframe
personId = list(main_dict.keys())
misses = []
for i in range(len(personId)):
    misses.append(main_dict[personId[i]])

stat = pd.DataFrame({"Name": wcaname(personId), "Country": wcacountry(personId), "Missed Chances": misses})
if __name__ == "__main__":
    print(stat.sort_values("Missed Chances", ascending=False).reset_index(drop="index").head(10))
    stat.to_csv(f"unlucky {event}.csv", index=False)

# Second DF
mc = pd.DataFrame(
    {"Name": wcaname(wcaids), "Country": wcacountry(wcaids), "Competition": komp, "Best Possible Average": bpa,
     "Current WR": cwr, "Minimum Time Needed": mint, "Solve1": v1, "Solve2": v2, "Solve3": v3, "Solve4": v4})

if __name__ == "__main__":
    mc.to_csv(f"unlucky {event} breakdown.csv", index=False)

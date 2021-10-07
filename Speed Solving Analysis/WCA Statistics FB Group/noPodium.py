import pandas as pd
from datetime import datetime

# Best results for each event not to podium

low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

finals = results[results.roundTypeId == "f"].reset_index(drop="index")

retired_events = ["magic", "mmagic", "333mbo", "333ft"]
singlevents = ["333bf", "444bf", "555bf", "333mbf"]
events = finals.eventId.unique()


# Functions
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


def mbldpoints(T):
    z = []
    for t in T:
        dt = (t - (t % 10 ** 7)) / 10 ** 7
        z.append(99 - dt)
    return z


# Columns
eve = []
wcaids = []
avg = []
komp = []
print("Started Loop")
for event in events:
    if event not in retired_events:
        u = datetime.now()
        print(f"Started {event}")
        if event == "333mbf":
            mintime = 0
        else:
            mintime = 360_000
        minid = "2017STOK03"
        mincomp = "WC2003"
        data = finals[finals.eventId == event].reset_index(drop="index")
        komps = data.competitionId.unique()
        # Loop through competitions
        for comp in komps:
            x = data[data.competitionId == comp].sort_values("pos").reset_index(drop="index")
            if len(x) > 3:
                if event not in singlevents and x.average[3] > 0:
                    if x.average[3] < mintime:
                        mintime = x.average[3]
                        minid = x.personId[3]
                        mincomp = comp
                elif x.best[3] > 0:
                    if event in singlevents and event != "333mbf" and x.best[3] < mintime:
                        mintime = x.best[3]
                        minid = x.personId[3]
                        mincomp = comp
                    elif event == "333mbf" and mbldpoints([x.best[3]])[0] > mintime:
                        mintime = mbldpoints([x.best[3]])[0]
                        minid = x.personId[3]
                        mincomp = comp

        # Table Entries
        eve.append(event)
        wcaids.append(minid)
        if event == "333mbf":
            avg.append(mintime)
        else:
            avg.append(round(mintime / 100, 2))
        komp.append(mincomp)

        t = datetime.now()
        dt = t - u
        print(f"Completed {event} in {dt.seconds} seconds.")

df = pd.DataFrame({"Event": eve, "Time": avg, "Name": wcaname(wcaids), "Country": wcacountry(wcaids),
                   "Competition": komp})

if __name__ == "__main__":
    df.to_csv("nopodium.csv", index=False)

# Imports
import pandas as pd
import numpy as np
from datetime import datetime

# Data Frames
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')

# Dictionaries
events = results.eventId.unique()
len_events = len(events)
events_dict = {}
print("Events dictionary started.")
for e in range(len(events)):
    events_dict[events[e]] = e
print("Events dictionary finished.")

print("ELO dictionary started.")
elo_dict = {}
scratch = True
persons = results.personId.nunique()
personlist = results.personId.unique()
if not scratch:
    elotable400 = pd.read_csv("elotable_400.csv")
    for wcaid in list(elotable400.columns):
        elo_dict[wcaid] = list(elotable400[wcaid])
print("ELO dictionary finished.")


# Functions
def elo(home, away, lam=0.02):
    h = 1 - 1 / (1 + np.exp(lam * (away - home)))
    a = - 1 / (1 + np.exp(lam * (home - away)))
    return [h, a]

def round_finder(competition, event, rtype=""):
    df = results[results["competitionId"] == competition].reset_index(drop="index")
    df = df[["eventId", "roundTypeId", "pos", "personId"]]
    dfe = df[df["eventId"] == event].reset_index(drop="index")
    if rtype == "":
        return dfe
    else:
        dfer = dfe[dfe["roundTypeId"] == rtype].reset_index(drop="index")
        return dfer


def elo_calculator(competition, lam=0.2, mult=1600, eps=0.9999):
    df = results[results["competitionId"] == competition].reset_index(drop="index")
    df_events = df.eventId.unique()
    for event in df_events:
        edex = events_dict[event]
        dfe = round_finder(competition, event)
        eventids = dfe.personId.unique()
        for rtype in dfe.roundTypeId.unique():
            dfer = round_finder(competition, event, rtype)
            for i in range(len(dfer.pos)):
                homewcaid = dfer.personId[i]
                if homewcaid not in elo_dict.keys():
                    elo_dict[homewcaid] = [-1] * len(events)
                if elo_dict[homewcaid][edex] == -1:
                    elo_dict[homewcaid][edex] = 1000  # default elo is 1000
                for j in range(len(dfer.pos)):
                    if i < j:
                        awaywcaid = dfer.personId[j]
                        if awaywcaid not in elo_dict.keys():
                            elo_dict[awaywcaid] = [-1] * len(events)
                        if elo_dict[awaywcaid][edex] == -1:
                            elo_dict[awaywcaid][edex] = 1000
                        points = elo(elo_dict[homewcaid][edex], elo_dict[awaywcaid][edex], lam)
                        elo_dict[homewcaid][edex] += mult / len(dfer) * points[0]
                        if elo_dict[awaywcaid][edex] + mult / len(dfer) * points[1] < 0:
                            elo_dict[awaywcaid][edex] = 0
                        else:
                            elo_dict[awaywcaid][edex] += mult / len(dfer) * points[1]
        for wcaid in list(elo_dict.keys()):
            if wcaid not in eventids:
                score = elo_dict[wcaid][edex]
                if score > 0:
                    elo_dict[wcaid][edex] = score * eps


# Calculates the ELO score for every competitor
count = 0
if scratch:
    start_val = 0
else:
    start_val = 0
total_comps = results.competitionId.nunique()
list_comps = results.competitionId.unique()
init_t = datetime.now()
start = True
if start:
    print("Started")
    for competition in list_comps:
        if count > start_val:
            elo_calculator(competition)
        count += 1
        if count % int(total_comps / 1000) == 0 and count > start_val:
            print("Last competition entered: " + competition)
            print("Percent complete: " + str(round(100 * count / total_comps, 2)) + "%")
            if count == start_val + 7 - start_val % 7:
                print("Elapsed time:", datetime.now() - init_t)
            else:
                print("Elapsed time:", datetime.now() - t)
                print("Total elapsed time:", datetime.now() - init_t)
            t = datetime.now()
        if count % 100 == 0 and count > start_val:
            elotable = pd.DataFrame(elo_dict)
            elotable.to_csv("elotable_" + str(count) + ".csv", index=False)
            print("=" * 50)
            print("Elapsed time for " + str(count) + " comps:", datetime.now() - init_t)
            print("=" * 50)
    print("Finished")
    print("Elapsed time:", datetime.now() - init_t)

# Creates the CSV file
if not start:
    print("Started WC2003")
    elo_calculator("WC2003", 0.2, 1600)
    print("Started WC2005")
    elo_calculator("WC2005", 0.2, 1600)
    print("Started WC2007")
    elo_calculator("WC2007", 0.2, 1600)
    print("Started WC2009")
    elo_calculator("WC2009", 0.2, 1600)
    print("Started WC2011")
    elo_calculator("WC2011", 0.2, 1600)
    print("Started WC2013")
    elo_calculator("WC2013", 0.2, 1600)
    print("Started WC2015")
    elo_calculator("WC2015", 0.2, 1600)
    print("Started WC2017")
    elo_calculator("WC2017", 0.2, 1600)
    print("Started WC2019")
    elo_calculator("WC2019", 0.2, 1600)
    print("Finished")

elo_table = {}
elo_table["personId"] = list(elo_dict.keys())
for e in range(len(events)):
    event = events[e]
    elo_table[event] = []
    for wcaid in list(elo_dict.keys()):
        score = elo_dict[wcaid][e]
        elo_table[event].append(round(score, 2))

elo_df = pd.DataFrame(elo_table)
if not start:
    print(elo_df.sort_values("333", ascending=False).reset_index(drop="index").head(10))
if start:
    elo_df.to_csv("wca_elo_rankings.csv", index=False)

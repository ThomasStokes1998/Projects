# Imports
import pandas as pd
import numpy as np
from datetime import datetime

# Data Frames
low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
championships = pd.read_csv('WCA Database/WCA_export_championships.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

champs = championships.competition_id.unique()
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
scratch = False
#persons = results.personId.nunique()
personlist = results.personId.unique()
if not scratch:
    ncomps = 7080
    elotable_scratch = pd.read_csv("elotable_" + str(ncomps) + ".csv")
    for wcaid in list(elotable_scratch.columns):
        elo_dict[wcaid] = list(elotable_scratch[wcaid])
print("ELO dictionary finished.")


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


def compdate(comp):
    df = competitions[competitions.id == comp].reset_index(drop="index")
    month = df.month[0]
    year = df.year[0]
    date = str(month) + "_" + str(year)
    return date


def elo(home, away, lam=0.02):
    h = 1 - 1 / (1 + np.exp(lam * (away - home)))
    a = - 1 / (1 + np.exp(lam * (home - away)))
    return [h, a]


def elo_weight(rtype, competition):
    mult = 1
    if competition in champs:
        mult = 1.5
    if "wc20" in competition.lower():
        mult = 2
    if rtype == "1":
        return 10 * mult
    if rtype == "2":
        return 20 * mult
    if rtype == "3":
        return 25 * mult
    if rtype == "f":
        return 50 * mult
    else:
        return 20 * mult


def round_finder(competition, event, rtype=""):
    df = results[results["competitionId"] == competition].reset_index(drop="index")
    df = df[["eventId", "roundTypeId", "pos", "personId", "regionalSingleRecord", "regionalAverageRecord"]]
    df["regionalSingleRecord"] = df["regionalSingleRecord"].fillna("0")
    df["regionalAverageRecord"] = df["regionalAverageRecord"].fillna("0")
    dfe = df[df["eventId"] == event].reset_index(drop="index")
    if rtype == "":
        return dfe
    else:
        dfer = dfe[dfe["roundTypeId"] == rtype].reset_index(drop="index")
        return dfer


def elo_calculator(competition, lam=0.02):
    df = results[results["competitionId"] == competition].reset_index(drop="index")
    df_events = df.eventId.unique()
    for event in df_events:
        edex = events_dict[event]
        dfe = round_finder(competition, event)
        for rtype in dfe.roundTypeId.unique():
            dfer = round_finder(competition, event, rtype)
            dfer = dfer.sort_values("pos").reset_index(drop='index')
            elow = elo_weight(rtype, competition)
            for i in range(len(dfer.pos)):
                homewcaid = dfer.personId[i]
                # Adds new WCAID
                if homewcaid not in elo_dict.keys():
                    elo_dict[homewcaid] = [-1] * len(events)
                if elo_dict[homewcaid][edex] == -1:
                    elo_dict[homewcaid][edex] = 1000  # default elo is 1000
                for j in range(len(dfer.pos)):
                    if i < j:  # Saves looping through half the possible i / j values
                        awaywcaid = dfer.personId[j]
                        # Adds new WCAID
                        if awaywcaid not in elo_dict.keys():
                            elo_dict[awaywcaid] = [-1] * len(events)
                        if elo_dict[awaywcaid][edex] == -1:
                            elo_dict[awaywcaid][edex] = 1000
                        points = elo(elo_dict[homewcaid][edex], elo_dict[awaywcaid][edex], lam)
                        # Points for 'home'
                        elo_dict[homewcaid][edex] += elow * points[0]
                        # Points for 'away'
                        if elo_dict[awaywcaid][edex] + elow * points[1] < 0:
                            elo_dict[awaywcaid][edex] = 0
                        else:
                            elo_dict[awaywcaid][edex] += elow * points[1]
                # Points for records
                if dfer["regionalSingleRecord"][i] == "NR":
                    elo_dict[homewcaid][edex] += 10
                elif dfer["regionalSingleRecord"][i] == "WR":
                    elo_dict[homewcaid][edex] += 50
                elif dfer["regionalSingleRecord"][i] != "0":
                    elo_dict[homewcaid][edex] += 20
                if dfer["regionalAverageRecord"][i] == "NR":
                    elo_dict[homewcaid][edex] += 10
                elif dfer["regionalAverageRecord"][i] == "WR":
                    elo_dict[homewcaid][edex] += 50
                elif dfer["regionalAverageRecord"][i] != "0":
                    elo_dict[homewcaid][edex] += 20


# Calculates the ELO score for every competitor
count = 0
if scratch:
    start_val = 0
else:
    start_val = ncomps
total_comps = results.competitionId.nunique()
list_comps = results.competitionId.unique()
init_t = datetime.now()
comp_date = "08_2021"
start = True
if start:
    print("Started")
    for competition in list_comps:
        if count > start_val:
            elo_calculator(competition)
            # Depreciates existing scores at the beginning of each month
            comp_date1 = compdate(competition)
            if comp_date1 != comp_date:
                for wcaid in list(elo_dict.keys()):
                    for e in range(len(events)):
                        score = elo_dict[wcaid][e]
                        if score > 0:
                            elo_dict[wcaid][e] = score * 0.995
            # Updates the current month only useful if calculating comps over more than a month
            comp_date = comp_date1
        count += 1
        # Keeping track of progress
        if count % int(total_comps / 1000) == 0 and count > start_val:
            print("-" * 30 + comp_date + "-" * 30)
            print("Last competition entered: " + competition)
            print("Percent complete: " + str(round(100 * count / total_comps, 2)) + "%")
            if count == start_val + 7 - start_val % 7:
                print("Elapsed time:", datetime.now() - init_t)
            else:
                print("Elapsed time:", datetime.now() - t)
                print("Total elapsed time:", datetime.now() - init_t)
            t = datetime.now()
        # Creating regular saves (every 100 comps) incase the program crashes
        # This code is largely redundant as long as I don't decide to restart in the future
        if count % 100 == 0 and count > start_val:
            elotable = pd.DataFrame(elo_dict)
            elotable.to_csv("elotable_" + str(count) + ".csv", index=False)
            if count - start_val == 100:
                print("=" * 20 + competition + "=" * 20)
                print("Elapsed time for " + str(count) + " comps:", datetime.now() - init_t)
                print("=" * 20 + competition + "=" * 20)
                m = datetime.now()
            else:  # Probably can be deleted (see previous comment)
                print("=" * 20 + competition + "=" * 20)
                print("Elapsed time for " + str(count) + " comps:", datetime.now() - m)
                print("=" * 20 + competition + "=" * 20)
                m = datetime.now()
    # Complete ELO Table
    elotable = pd.DataFrame(elo_dict)
    elotable.to_csv("elotable_" + str(count) + ".csv", index=False)
    print("Finished")
    print("Elapsed time:", datetime.now() - init_t)

# Creates the CSV file
retired_events = ["magic", "mmagic", "333mbo", "333ft"]
elo_table = {}
elo_table["personId"] = list(elo_dict.keys())
elo_table["overall"] = []
for wcaid in list(elo_dict.keys()):
    total_score = 0  # For overall score
    for event in events:
        if event not in retired_events and event not in list(elo_table.keys()):
            elo_table[event] = []
        if event not in retired_events:
            e = events_dict[event]
            score = elo_dict[wcaid][e]
            if score > 0:
                total_score += score
            elo_table[event].append(round(score))
    elo_table["overall"].append(round(total_score / 17))

elo_df = pd.DataFrame(elo_table)
if not start:
    print(elo_df.sort_values("333", ascending=False).reset_index(drop="index").head(10))  # ELO test
if start:
    elo_df.to_csv("wca_elo_rankings.csv", index=False)
    # Creating CSV files for Github Repo
    elodf = pd.read_csv("wca_elo_rankings.csv")
    # elodf = elodf.drop(retired_events, axis=1)
    for event in elodf.columns:
        if event != "personId":
            print("Started " + event)
            # Finds the top 1000 elos for each event
            d = elodf[["personId", event]]
            y = d.sort_values(event, ascending=False).reset_index(drop="index")
            y = y[:1000]
            y["name"] = wcaname(y["personId"])
            y["country"] = wcacountry(y["personId"])
            y = y[["name", "country", event]]
            y.to_csv("top_1000_elo_" + event + ".csv", index=False)
            print("Finished " + event)

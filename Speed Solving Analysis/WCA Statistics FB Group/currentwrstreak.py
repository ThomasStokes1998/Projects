import pandas as pd
from datetime import date

low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

# WCA Stats current longest WR streak but it doesn't reset when broken by the same person
wrsingles = results[results.regionalSingleRecord == "WR"].reset_index(drop="index")
wraverages = results[results.regionalAverageRecord == "WR"].reset_index(drop="index")


def comp_date(complist):
    dates = []
    for c in complist:
        cinfo = competitions[competitions.id == c].reset_index(drop="index")
        y = cinfo.year[0]
        m = cinfo.month[0]
        d = cinfo.day[0]
        dates.append(date(y, m, d))
    return dates


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
            print(wcaid)
            z.append(wcaid)
        else:
            z.append(x[len(x) - 1])
    return z


wrsingles["date"] = comp_date(wrsingles.competitionId)
wraverages["date"] = comp_date(wraverages.competitionId)

wrsingles = wrsingles.sort_values("date", ascending=False).reset_index(drop="index")
wraverages = wraverages.sort_values("date", ascending=False).reset_index(drop="index")

events = results.eventId.unique()
retired_events = ["333mbo", "magic", "mmagic", "333ft"]
personIds = []
types = []
streaks = []
sdates = []
for event in events:
    if event not in retired_events:
        # Single WR History
        evsingle = wrsingles[wrsingles.eventId == event].reset_index(drop="index")
        l = len(evsingle)
        wcaid = evsingle.personId[0]
        for i in range(l):
            if evsingle.personId[i] != wcaid:
                sd = evsingle.date[i - 1]
                streak = (date.today() - sd).days
                personIds.append(wcaid)
                types.append(event + " single")
                streaks.append(streak)
                sdates.append(sd)
                break
        # Average WR History
        evaverage = wraverages[wraverages.eventId == event].reset_index(drop="index")
        l = len(evaverage)
        if l > 0:
            wcaid = evaverage.personId[0]
            for i in range(l):
                if evaverage.personId[i] != wcaid:
                    sd = evaverage.date[i - 1]
                    streak = (date.today() - sd).days
                    personIds.append(wcaid)
                    types.append(event + " average")
                    streaks.append(streak)
                    sdates.append(sd)
                    break

# Making the CSV File
df = pd.DataFrame({"Name": wcaname(personIds), "Country": wcacountry(personIds), "Days": streaks, "Type": types,
                   "Since": sdates})

df = df.sort_values("Days", ascending=False).reset_index(drop="index")
if __name__ == "__main__":
    df.to_csv("currentwrstreak.csv", index=False)
    print(df[["Name", "Days", "Type", "Since"]].head(10))

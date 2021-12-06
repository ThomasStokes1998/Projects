import pandas as pd
from datetime import date

low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')

# WCA Stats longest WR streak but it doesn't reset when broken by another person
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

wrsingles = wrsingles.sort_values("date").reset_index(drop="index")
wraverages = wraverages.sort_values("date").reset_index(drop="index")

events = results.eventId.unique()
retired_events = ["333mbo", "magic", "mmagic", "333ft"]
type_dict = {}
streak_dict = {}
sdate_dict = {}
edate_dict = {}
for event in events:
    if event not in retired_events:
        # Single WR History
        evsingle = wrsingles[wrsingles.eventId == event].reset_index(drop="index")
        l = len(evsingle)
        for i in range(l):
            wcaid = evsingle.personId[i]
            if i == 0 or event == "333" and i == 1:
                currholder = wcaid
                startdate = evsingle.date[i]
            elif wcaid != currholder:
                enddate = evsingle.date[i]
                streak = (enddate - startdate).days
                if currholder not in type_dict:
                    type_dict[currholder] = event + " single"
                    streak_dict[currholder] = streak
                    sdate_dict[currholder] = startdate
                    edate_dict[currholder] = enddate
                elif streak > streak_dict[currholder]:
                    type_dict[currholder] = event + " single"
                    streak_dict[currholder] = streak
                    sdate_dict[currholder] = startdate
                    edate_dict[currholder] = enddate
                currholder = wcaid
                startdate = enddate
            if i == l - 1:
                enddate = date.today()
                streak = (enddate - startdate).days
                if currholder not in type_dict:
                    type_dict[currholder] = event + " single"
                    streak_dict[currholder] = streak
                    sdate_dict[currholder] = startdate
                    edate_dict[currholder] = enddate
                elif streak > streak_dict[currholder]:
                    type_dict[currholder] = event + " single"
                    streak_dict[currholder] = streak
                    sdate_dict[currholder] = startdate
                    edate_dict[currholder] = enddate
        # Average WR History
        evaverage = wraverages[wraverages.eventId == event].reset_index(drop="index")
        l = len(evaverage)
        if l > 0:
            for i in range(l):
                wcaid = evaverage.personId[i]
                if i == 0:
                    currholder = wcaid
                    startdate = evaverage.date[i]
                elif wcaid != currholder:
                    enddate = evaverage.date[i]
                    streak = (enddate - startdate).days
                    if currholder not in type_dict:
                        type_dict[currholder] = event + " average"
                        streak_dict[currholder] = streak
                        sdate_dict[currholder] = startdate
                        edate_dict[currholder] = enddate
                    elif streak > streak_dict[currholder]:
                        type_dict[currholder] = event + " average"
                        streak_dict[currholder] = streak
                        sdate_dict[currholder] = startdate
                        edate_dict[currholder] = enddate
                    currholder = wcaid
                    startdate = enddate
                if i == l - 1:
                    enddate = date.today()
                    streak = (enddate - startdate).days
                    if currholder not in type_dict:
                        type_dict[currholder] = event + " average"
                        streak_dict[currholder] = streak
                        sdate_dict[currholder] = startdate
                        edate_dict[currholder] = enddate
                    elif streak > streak_dict[currholder]:
                        type_dict[currholder] = event + " average"
                        streak_dict[currholder] = streak
                        sdate_dict[currholder] = startdate
                        edate_dict[currholder] = enddate

# Making the CSV File
personids = []
streaks = []
types = []
startdates = []
enddates = []
for wcaid in type_dict:
    personids.append(wcaid)
    streaks.append(streak_dict[wcaid])
    types.append(type_dict[wcaid])
    startdates.append(sdate_dict[wcaid])
    enddates.append(edate_dict[wcaid])

df = pd.DataFrame({"Name": wcaname(personids), "Country": wcacountry(personids), "Streak": streaks, "Type": types,
                   "Start Date": startdates, "End Date": enddates})

df = df.sort_values("Streak", ascending=False).reset_index(drop="index")
if __name__ == "__main__":
    df.to_csv("longestwrstreak.csv", index=False)
    print(df[["Name", "Streak", "Type"]].head(10))

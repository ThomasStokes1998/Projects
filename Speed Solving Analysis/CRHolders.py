import pandas as pd
from datetime import date, datetime
from almostWR import ordercompdf, getCompdate

# Data Frames
low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')
countries = pd.read_csv("WCA Database/WCA_export_Countries.tsv", delimiter="\t")

# print(countries.info())
# print(countries.head(10))


ordercompdf()

events = results.eventId.unique()
retired_events = ["magic", "mmagic", "333mbo", "333ft"]


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


def getCRtype(cr):
    if cr == "AfR":
        return "_Africa"
    if cr == "AsR":
        return "_Asia"
    if cr == "ER":
        return "_Europe"
    if cr == "NaR":
        return "_North America"
    if cr == "OcR":
        return "_Oceania"
    if cr == "SaR":
        return "_South America"


def getCont(nations):
    gct = []
    for nation in nations:
        for i in range(len(countries)):
            if countries.id[i] == nation:
                gct.append(countries.continentId[i])
                break
    return gct


def getWRs(event="333"):
    eve = results[results.eventId == event].reset_index(drop="index")
    evewra = eve[eve.regionalAverageRecord == "WR"].reset_index(drop="index")
    evewra["date"] = getCompdate(evewra.competitionId)
    evewra["type"] = ["A"] * len(evewra)
    evewrs = eve[eve.regionalSingleRecord == "WR"].reset_index(drop="index")
    evewrs["date"] = getCompdate(evewrs.competitionId)
    evewrs["type"] = ["S"] * len(evewrs)
    evewr = evewrs.merge(evewra, how="outer")
    return evewr.sort_values("date").reset_index(drop="index")


def getCR(cr, event, type=None):
    eve = results[results.eventId == event].reset_index(drop="index")
    dfcrs = eve[eve.regionalSingleRecord == cr].reset_index(drop="index")
    dfcra = eve[eve.regionalAverageRecord == cr].reset_index(drop="index")
    dfcrs["date"] = getCompdate(dfcrs.competitionId)
    dfcrs["type"] = ["S"] * len(dfcrs)
    dfcra["date"] = getCompdate(dfcra.competitionId)
    dfcra["type"] = ["A"] * len(dfcra)
    df = dfcrs.merge(dfcra, how="outer")
    gcr = df.merge(getWRs(event), how="outer")
    gcr["continentId"] = getCont(gcr.personCountryId)
    gcr = gcr[gcr.continentId == getCRtype(cr)].reset_index(drop="index")
    if type == "S" or type == "A":
        gcr = gcr[gcr["type"] == type].reset_index(drop="index")
    gcr = gcr.sort_values("date").reset_index(drop="index")
    return gcr[["personId", "eventId", "personCountryId", "date", "best", "average", "type"]]


def allCRs(cr, progress=True):
    cr_dict = {}
    new = True
    if progress:
        u_ = datetime.now()
    for event in events:
        for t in ["S", "A"]:
            cr_dict[event + t] = getCR(cr, event, t)
            if new:
                all = cr_dict[event + t]
                new = False
            else:
                all = all.merge(cr_dict[event + t], how="outer")
    cr_dict["all"] = all.sort_values("date").reset_index(drop="index")
    if progress:
        dt = datetime.now() - u_
        print(f"Finished dictionary in {dt.seconds} seconds.")
    return cr_dict


def toDate(dates):
    td = []
    for d in dates:
        dd = d % 100
        dd = round(dd)
        mm = (d % 10 ** 4 - dd) / 100
        mm = round(mm)
        yy = (d - d % 10 ** 4) / 10 ** 4
        yy = round(yy)
        # print([yy, mm, dd])
        td.append(date(yy, mm, dd))
    return td


# main loop
# Columns
record_holders = []
country = []
longest_streak = []
start_dates = []
end_dates = []
for cr in ["AfR", "AsR", "ER", "NaR", "OcR", "SaR"]:
    print("Starting " + getCRtype(cr)[1:])
    u = datetime.now()
    cr_dict = allCRs(cr)
    all = cr_dict["all"]
    ids = all.personId.unique()
    count = 0
    for wcaid in ids:
        record_holders.append(wcaid)
        records = all[all.personId == wcaid].reset_index(drop="index")
        l = len(records)
        country.append(records.personCountryId[l - 1])
        lstreak = 0
        record_hist = {}
        init_start = 0
        # Creates a dictionary containing start and end dates for all CRs
        for i in range(l):
            start = records.date[i]
            start_time = toDate([start])[0]
            if init_start == 0 and start_time.year >= 2003:
                init_start = start_time
            record_types = list(record_hist.keys())
            if start_time.year >= 2003:
                ev = records.eventId[i]
                ty = records.type[i]
                if ev + ty not in record_types or ev + ty in record_types and start_time > \
                        record_hist[ev + ty][len(record_hist[ev + ty]) - 1][1]:
                    crhist = cr_dict[ev + ty]
                    minj = -1
                    # Finds when they lost the CR
                    for j in range(len(crhist)):
                        if crhist.personId[j] == wcaid and minj == -1 and crhist.date[j] == start:
                            minj = j
                        elif j > minj > -1 and crhist.personId[j] != wcaid:
                            end = crhist.date[j]
                            end_time = toDate([end])[0]
                            break
                        if j == len(crhist) - 1:
                            if ev not in retired_events:
                                end_time = date.today()
                            elif ev == "333ft":
                                end_time = date(2020, 1, 1)
                            elif ev == "333mbo":
                                end_time = date(2010, 1, 1)
                            else:
                                end_time = date(2013, 1, 1)
                    if ev + ty not in record_types:
                        record_hist[ev + ty] = [[start_time, end_time]]
                    elif ev + ty in record_types and start_time > record_hist[ev + ty][len(record_hist[ev + ty]) - 1][
                        1]:
                        record_hist[ev + ty].append([start_time, end_time])
        # Finding the longest streak
        eventype = []
        start_times = []
        end_times = []
        for evty in record_types:
            y = record_hist[evty]
            for x in y:
                eventype.append(evty)
                start_times.append(x[0])
                end_times.append(x[1])
        et = pd.DataFrame({"ET": eventype, "STT": start_times, "ENT": end_times})
        et = et.sort_values("STT").reset_index(drop="index")
        if len(et) == 0:
            longest_streak.append(0)
            start_dates.append(date(2003, 1, 1))
            end_dates.append(date(2003, 1, 1))
        else:
            curr_stt = et["STT"][0]
            max_stt = et["STT"][0]
            curr_ett = et["ENT"][0]
            max_ett = et["ENT"][0]
            diff = max_ett - max_stt
            max_streak = diff.days
            L = len(et)
            c = datetime.now()
            while L > 0:
                df = et[et["STT"] > curr_ett].reset_index(drop="index")
                L = len(df)
                if L == 0:
                    break
                else:
                    curr_stt = df["STT"][0]
                    curr_ett = df["ENT"][0]
                    for k in range(L):
                        if df["STT"][k] < curr_ett < df["ENT"][k]:
                            curr_ett = df["ENT"][k]
                        if df["STT"][k] > curr_ett:
                            break
                    diff = curr_ett - curr_stt
                    streak = diff.days
                    if streak > max_streak:
                        max_stt = curr_stt
                        max_ett = curr_ett
                        max_streak = streak
                c1 = datetime.now() - c
                if c1.seconds > 10:
                    print(f"Might be stuck in an infinite loop.")
                    print("wcaid: " + wcaid)
                    print("=" * 50)
                    print(et)
                    print("=" * 50)
                    print(df)
                    print("=" * 50)
                    break
            # Appending the items to the dataframe
            longest_streak.append(max_streak)
            start_dates.append(max_stt)
            end_dates.append(max_ett)
            count += 1
        if count % 10 == 0:
            print(f"Done {count} competitors at {datetime.now()}.")
    t = datetime.now()
    dt = t - u
    print("Finished " + getCRtype(cr)[1:] + f" in {dt}.")

if __name__ == "__main__":
    crs = pd.DataFrame({"Name": wcaname(record_holders), "Country": country, "Max Streak (days)": longest_streak,
                        "Start Date": start_dates, "End Date": end_dates})
    crs = crs.sort_values("Max Streak (days)", ascending=False).reset_index(drop="index")
    crs.to_csv("crstreak.csv", index=False)

import pandas as pd

rsingle = pd.read_csv('WCA Database/WCA_export_RanksSingle.tsv', delimiter='\t')
raverage = pd.read_csv('WCA Database/WCA_export_RanksAverage.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')
rsingle["eventId"] = rsingle["eventId"].apply(lambda x: str(x))
raverage["eventId"] = raverage["eventId"].apply(lambda x: str(x))
print(rsingle.info())


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


italians = persons[persons.countryId == "Italy"].id
estonians = persons[persons.countryId == "Estonia"].id

rank = []
events = []

li = len(italians)
print(f"Started {li} Italians")
count = 0
for italian in italians:
    count += 1
    singles = rsingle[rsingle.personId == italian].sort_values("worldRank").reset_index(drop="index")
    if len(singles) == 0:
        rank.append(150_000)
        events.append("Null")
    else:
        max_rank = singles.worldRank[0]
        max_event = singles.eventId[0]
        averages = raverage[raverage.personId == italian].sort_values("worldRank").reset_index(drop="index")
        if len(averages) > 0:
            a = averages.worldRank[0]
            if a < max_rank:
                max_rank = a
                max_event = averages.eventId[0]
        rank.append(max_rank)
        events.append(max_event)
    if count % 100 == 0:
        print(f"{(100 * count) // li}% complete.")

df = pd.DataFrame({"Name": wcaname(italians), "Best WR": rank, "Event": events})
df.sort_values("Best WR").reset_index(drop="index").to_csv("bestWR_Italy.csv", index=False)

rank = []
events = []

le = len(estonians)
print(f"Started {le} Estonians.")
count = 0
for estonian in estonians:
    count += 1
    singles = rsingle[rsingle.personId == estonian].sort_values("worldRank").reset_index(drop="index")
    if len(singles) == 0:
        rank.append(150_000)
        events.append("Null")
    else:
        max_rank = singles.worldRank[0]
        max_event = singles.eventId[0]
        averages = raverage[raverage.personId == estonian].sort_values("worldRank").reset_index(drop="index")
        if len(averages) > 0:
            a = averages.worldRank[0]
            if a < max_rank:
                max_rank = a
                max_event = averages.eventId[0]
        rank.append(max_rank)
        events.append(max_event)
    if count % 100 == 0:
        print(f"{(100 * count) // le}% complete.")

df = pd.DataFrame({"Name": wcaname(estonians), "Best WR": rank, "Event": events})
df.sort_values("Best WR").reset_index(drop="index").to_csv("bestWR_Estonia.csv", index=False)

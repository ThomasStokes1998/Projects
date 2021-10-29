import pandas as pd

low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')

# A function that checks how many solves someone has done in a competition

def competitionSolves(wcaid: str, compid: str):
    solves = results[results.personId == wcaid].reset_index(drop="index")
    compsolves = solves[solves.competitionId == compid].reset_index(drop="index")
    lcs = len(compsolves)
    if lcs == 0:
        return print("Enter a valid competition or wcaid.")
    total_solves = 0
    for i in range(lcs):
        eventid = compsolves.eventId[i]
        # See README.md file in WCA DB for how multibld results are encoded
        if eventid == "333mbf":
            for j in range(1, 6):
                attempt = compsolves[f"value{j}"][i]
                if attempt > 0:
                    dd = attempt // 10_000_000
                    mm = attempt % 100
                    total_solves += 99 - dd + mm
        elif eventid == "333mbo":
            for j in range(1, 6):
                attempt = compsolves[f"value{j}"][i]
                if attempt > 0:
                    x = attempt // 10_000_000
                    total_solves += 199 - x
        else:
            for j in range(1, 6):
                if compsolves[f"value{j}"][i] > 0:
                    total_solves += 1
    return total_solves


if __name__ == "__main__":
    print(competitionSolves("2020DWOR01", "MontpellierOpen2021"))

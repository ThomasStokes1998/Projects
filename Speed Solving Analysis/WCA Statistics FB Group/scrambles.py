import pandas as pd 
from RubiksCube2 import Cube2

rc = Cube2()

scrambles = pd.read_csv("WCA Database/WCA_export_Scrambles.tsv", delimiter="\t")
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')

def find4MoveScrambles(country:str) -> list:
    scrambles2x2 = scrambles[scrambles.eventId == "222"].reset_index(drop="index")
    country_comps = list(competitions[competitions.countryId == country].id)
    compcol = []
    fourmovescrambles = []
    for comp in country_comps:
        comp_scramble_table = scrambles2x2[scrambles2x2.competitionId == comp].reset_index(drop="index")
        for scr in comp_scramble_table.scramble:
            if rc.solveKorf(4, scr, findingdepth=False, finalphase=True)[0] is None:
                continue
            compcol.append(comp)
            fourmovescrambles.append(scr)
    pd.DataFrame({"comp":compcol, "scramble":fourmovescrambles}).to_csv(f"official4movescrambles_{country}.csv", index=False)
    return fourmovescrambles

if __name__ == "__main__":
    country = "France"
    fourmovescrambles = find4MoveScrambles(country)
    print(print(f"There have been {len(fourmovescrambles)} four move official scrambles in {country}."))

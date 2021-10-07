import pandas as pd

# Data Frames
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
comps = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')

# Defining some useful tables
mumbai_comps = comps[comps.cityName == "Mumbai, Maharashtra"].sort_values("year").reset_index(drop="index")
mumbai_comps = mumbai_comps[mumbai_comps.year >= 2017].id.unique()

# print(mumbai_comps) Testing we have the correct competitions

# We only need 3x3x3 results and since the results file is large we will use this to save computation time
three = results[results.eventId == "333"].reset_index(drop="index")

# Dataframe Columns
competitions = [] # Some competitions held in Mumbai (three since 2017 haven't) may not have 333
best_single_names = []
best_singles = []
best_average_names = []
best_averages = []

# Main Loop
for mc in mumbai_comps:
    df = three[three.competitionId == mc].reset_index(drop="index")
    l = len(df)
    if l > 0: # Filtering competitions with no 3x3x3
        single = False
        average = False
        for i in range(l):
            # Single Results
            df = df.sort_values("best").reset_index(drop="index")
            if df.best[i] > 0 and not single:
                best_single_names.append(df.personName[i])
                best_singles.append(df.best[i] / 100)
                single = True
            # Average Results
            df = df.sort_values("average").reset_index(drop="index")
            if df.average[i] > 0 and not average:
                best_average_names.append(df.personName[i])
                best_averages.append(df.average[i] / 100)
                average = True
            if single and average:
                competitions.append(mc) # Only append competition now because we know it has 3x3x3 as an event
                break # Stops the loop since we have all the values for the comp

# Creating the DataFrame

stat_req = pd.DataFrame({"Competition":competitions, "Best Single Name":best_single_names,
                         "Best Single":best_singles, "Best Average Names":best_averages,
                         "Best Average":best_averages})

if __name__ == "__main__":
    print(stat_req)
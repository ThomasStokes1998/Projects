# Imports
import pandas as pd
import numpy as np

# Data Frames
low_memory = False
results = pd.read_csv('WCA Database/WCA_export_Results.tsv', delimiter='\t')
competitions = pd.read_csv('WCA Database/WCA_export_Competitions.tsv', delimiter='\t')
championships = pd.read_csv('WCA Database/WCA_export_championships.tsv', delimiter='\t')
rsingle = pd.read_csv('WCA Database/WCA_export_RanksSingle.tsv', delimiter='\t')
raverage = pd.read_csv('WCA Database/WCA_export_RanksAverage.tsv', delimiter='\t')
persons = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')


class WcaFunctions:
    def __init__(self):
        # Import the dataframes into the class
        self.results = results
        self.competitions = competitions
        self.championships = championships
        self.rsingle = rsingle
        self.raverage = raverage
        self.persons = persons
        # Create new useful dataframes
        self.idindex = self.persons[self.persons.subid == 1].reset_index(drop="index")  # Removes Duplicate ID's

        # Clean the dataframes
        # Results
        self.results = self.results.drop(["personName", "personCountryId", "formatId"], axis=1)
        # Ranks
        self.rsingle["eventId"] = self.rsingle["eventId"].apply(lambda x: str(x))
        self.raverage["eventId"] = self.raverage["eventId"].apply(lambda x: str(x))
        # Persons
        self.persons["gender"] = self.persons["gender"].fillna("NB")
        self.idindex = self.idindex.drop(["subid"], axis=1)
        self.idindex["gender"] = self.idindex["gender"].fillna("NB")
        # Competitions
        self.competitions = self.competitions[
            ["id", "name", "cityName", "countryId", "year", "month", "day", "cancelled"]]

        # Useful lists
        self.wcaids = self.idindex.id.unique()
        self.comps = self.results.competitionId.unique()
        self.events = self.results.eventId.unique()
        self.retired_events = ["magic", "mmagic", "333mbo", "333ft"]

    # Returns all the official results for a given event
    def event_results(self, event, data=None):
        if data is None:
            data = self.results
        return data[data.eventId == event].reset_index(drop="index")

    # Returns all official results for a given wcaid
    def person_results(self, wcaid, data=None):
        if data is None:
            data = self.results
        return data[data.personId == wcaid].reset_index(drop="index")

    def competition_results(self, comp, data=None):
        if data is None:
            data = self.results
        return data[data.competitionId == comp].reset_index(drop="index")

    # Returns info for a given wcaid
    def person_info(self, wcaid):
        persondata = self.idindex[self.idindex.id == wcaid].reset_index(drop="index")
        return persondata

    # Returns the date of a list of competitions in dd-mm-yyyy format
    def comp_date(self, complist):
        dates = []
        for c in complist:
            cinfo = self.competitions[self.competitions.id == c].reset_index(drop="index")
            y = cinfo.year[0]
            m = cinfo.month[0]
            d = cinfo.day[0]
            dates.append(str(d) + "-" + str(m) + "-" + str(y))
        return dates

    # Returns all the competitors of a given country
    def country_competitors(self, country):
        return self.idindex[self.idindex.countryId == country].id.unique()

    # Returns all the competitions held a given country
    def country_competitions(self, country):
        reg = self.competitions[self.competitions.countryId == country].id.unique()
        ch = self.championships[self.championships.countryId == country].id.unique()
        return reg + ch

    # Finds everyone who has beaten a competitor in a given event
    def event_nemesis(self, wcaid, event, maxids=100):
        # Extracting the relevant data from the results dataframe
        ev = WcaFunctions.event_results(event)
        res = WcaFunctions.person_results(wcaid, data=ev)
        # Sorted such that worse finishes are at the top for more efficient loop
        res = res.sort_values("pos", ascending=False).reset_index(drop="index")
        nemeses = []
        comps = []
        for i in range(len(res)):
            p = res.pos[i]
            if p == 1:
                # If this is triggered we have exhausted all rounds where the competitor was beaten
                break
            else:
                c = res.competitionId[i] # Competition
                rt = res.roundTypeId[i] # Round
                df1 = WcaFunctions.competition_results(c, data=ev)
                df2 = df1[df1.roundTypeId == rt].sort_values("pos").reset_index(drop="index")
                for j in range(p - 1):
                    wcaid = df2.personId[j]
                    if wcaid not in nemeses: # To avoid Duplicates
                        nemeses.append(wcaid)
                        comps.append(c)
                        if len(nemeses) > maxids: # Enusres the list doesn't get too large
                            break
        # Convert the ids into names
        names = []
        for n in nemeses:
            nom = WcaFunctions.person_info(n).name[0]
            names.append(nom)
        # Make the final dataframe
        df = pd.DataFrame({"Name":names, "Competition":comps, "Date":WcaFunctions.comp_date(comps)})
        return df

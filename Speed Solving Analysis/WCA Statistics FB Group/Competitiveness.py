import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dg = pd.read_csv('WCA Database/WCA_export_RanksAverage.tsv', delimiter='\t')
dg.rename(columns={'best': 'average', 'personId': 'wcaId',
                   'worldRank': 'average_wr', 'continentRank': 'average_cr', 'countryRank': 'average_nr'},
          inplace=True)
dg['eventId'] = dg['eventId'].replace(333, '333')
dg['eventId'] = dg['eventId'].replace(222, '222')
dg['average'] = dg['average'].apply(lambda x: x / 100)

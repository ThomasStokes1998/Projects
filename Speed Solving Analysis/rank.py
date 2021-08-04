import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Load the data
df = pd.read_csv('WCA Database/WCA_export_RanksSingle.tsv', delimiter='\t')
dg = pd.read_csv('WCA Database/WCA_export_RanksAverage.tsv', delimiter='\t')
dp = pd.read_csv('WCA Database/WCA_export_Persons.tsv', delimiter='\t')
# Cleaning the data
df.rename(columns={'best': 'single', 'personId': 'wcaId',
                   'worldRank': 'single_wr', 'continentRank': 'single_cr', 'countryRank': 'single_nr'},
          inplace=True)
dg.rename(columns={'best': 'average', 'personId': 'wcaId',
                   'worldRank': 'average_wr', 'continentRank': 'average_cr', 'countryRank': 'average_nr'},
          inplace=True)

df['eventId'] = df['eventId'].replace(333, '333')
dg['eventId'] = dg['eventId'].replace(333, '333')
df['eventId'] = df['eventId'].replace(222, '222')
dg['eventId'] = dg['eventId'].replace(222, '222')

df['single'] = df['single'].apply(lambda x: x / 100)
dg['average'] = dg['average'].apply(lambda x: x / 100)


def repval(event, data, mult=100):
    col = []
    if data is df:
        for i in range(len(data['wcaId'])):
            if data['eventId'][i] == event:
                score = data['single'][i] * mult
                col.append(score)
            else:
                score = data['single'][i]
                col.append(score)
    if data is dg:
        for i in range(len(data['wcaId'])):
            if data['eventId'][i] == event:
                score = data['average'][i] * mult
                col.append(score)
            else:
                score = data['average'][i]
                col.append(score)
    return col


# df['single'] = repval('333fm', df)
# df['single'] = repval('333mbf', df)
# dg['average'] = repval('333fm', dg)
# dg['average'] = repval('333mbf', dg)

# Getting the column values
comp_sng = []
for event in df['eventId'].unique():
    de = df[df['eventId'] == event]
    pop = de['wcaId'].nunique()
    comp_sng.append(pop)

comp_avg = []
for event in dg['eventId'].unique():
    de = dg[dg['eventId'] == event]
    pop = de['wcaId'].nunique()
    comp_avg.append(pop)

# Creating the table
table_sng = pd.DataFrame({'Event': df['eventId'].unique(), 'Single': comp_sng})
table_avg = pd.DataFrame({'Event': dg['eventId'].unique(), 'Average': comp_avg})
table = pd.merge(table_sng, table_avg, how='left')

# 333mbf has no averages
table = table.fillna(0)

# Adding additional columns
table['AverageProp%'] = round(table['Average'] * 100 / table['Single'], 2)
table['Single%'] = round(table['Single'] * 100 / df['wcaId'].nunique(), 2)
table['Average%'] = round(table['Average'] * 100 / df['wcaId'].nunique(), 2)

# Viewing the table
table = table.sort_values('Single', ascending=False).reset_index(drop='index')
table = table.convert_dtypes(convert_integer=True)
table.to_csv('EventPopularity.csv', index=False)

print(table)


# Get's results for a given competitors (default is me)
def getresults(wcaid='2017STOK03', single=True, average=True):
    dsng = df[df['wcaId'] == wcaid].drop('wcaId', axis=1).reset_index(drop='index')
    davg = dg[dg['wcaId'] == wcaid].drop('wcaId', axis=1).reset_index(drop='index')
    if single == False and average == False:
        return 'Error: No input data!'
    if single == False:
        tbl = davg
        return tbl
    if average == False:
        tbl = dsng
        return tbl
    else:
        tbl = pd.merge(dsng, davg, how='left')
        return tbl


# print(getresults(single=False))
dsix = dg[dg['eventId'] == '666'].drop('eventId', axis=1)


def placement(event, time, single=False, average=False):
    if single == True:
        data = df[df['eventId'] == event][['wcaId', 'single', 'single_wr']]
        return data[data['single'] > (time - 0.01)]
    if average == True:
        data = dg[dg['eventId'] == event][['wcaId', 'average', 'average_wr']]
        return data[data['average'] > (time - 0.01)]


# print(placement('555', 91.58, average=True).head(10))


x_t = np.arange(110, 302, 2)
y_h = []
for t in x_t:
    dh = placement('777', t, average=True)
    y = list(dh.average_wr)
    y_h.append(y[0])
y_d = [y_h[i + 1] - y_h[i] for i in range(len(y_h) - 1)]
plt.style.use('fivethirtyeight')


# plt.scatter(np.arange(110, 300, 2), y_d, alpha=0.6)
# plt.xticks(np.arange(110, 310, 10))
# plt.yticks(np.arange(0, np.max(y_d), 4))
# plt.xlabel('Time(s)')
# plt.ylabel('Number of Competitors')
# plt.legend(['2s interval'])
# plt.title('The Density of 777 average results')


# plt.show()


def cat(event, time):
    data = df[df['eventId'] == event][['single', 'single_wr']]
    date = data[data['single'] > time].reset_index(drop='index')
    lst = date['single_wr']
    return lst[0]


def dog(event, time):
    data = dg[dg['eventId'] == event][['average', 'average_wr']]
    date = data[data['average'] > time].reset_index(drop='index')
    lst = date['average_wr']
    return lst[0]


# Relay times
def relay(wcaid):
    tbl_s = getresults(wcaid, average=False)
    tbl_a = getresults(wcaid, single=False)
    events = ['222', '333', '444', '555', '666', '777']
    time_s = 0
    time_a = 0
    for event in events:
        if event in tbl_s['eventId'].unique():
            score_s = tbl_s[tbl_s['eventId'] == event]["single"]
            time_s += score_s[0]
        else:
            time_s = 3600
            break
    for event in events:
        if event in tbl_a['eventId'].unique():
            score_a = tbl_a[tbl_a['eventId'] == event]["average"]
            time_a += score_a[0]
        else:
            time_a = 3600
            break
    return [round(time_s, 2), round(time_a, 2)]


# print(relay('2017STOK03'))

# Generates the WCA_Relay.csv Dataframe
def RelayTable(Generate=False):
    if Generate:
        relay_id = []
        relay_name = []
        relay_single = []
        relay_average = []
        count = 0
        avgs = dg[dg['eventId'] == '777']['wcaId'].unique()
        for id in avgs:
            r = relay(id)
            if r[0] < 1200 and r[1] < 1200:
                nom = str(dp[dp.id == id].name).split(' ')
                fname = nom[4]
                lname = nom[5].split('\n')[0]
                relay_id.append(id)
                relay_name.append(fname + ' ' + lname)
                relay_single.append(r[0])
                relay_average.append(r[1])
                count += 1
                if count % 100 == 0:
                    print(count)
        relay_table = pd.DataFrame(
            {'wcaId': relay_id, 'name': relay_name, 'single': relay_single, 'average': relay_average})
        cols = list(relay_table.columns)
        relay_table = relay_table.sort_values('single', ascending=True)
        relay_table['rank'] = np.arange(1, len(relay_name) + 1, 1)
        relay_table = relay_table[['rank'] + cols]
        relay_table.to_csv('WCA_relay.csv', index=False)
        print("Final Count:", count)


RelayTable(True)
dr = pd.read_csv('WCA_relay.csv')
dr.drop(['rank'], axis=1)
dr['rank'] = np.arange(1, len(dr.name) + 1, 1)
dr = dr[['rank', 'wcaId', 'name', 'single', 'average']]


# Histogram of times
def relayscore(X, single=False, average=False):
    means = np.mean(np.log1p(dr.single))
    stds = np.std(np.log1p(dr.single))
    meana = np.mean(np.log1p(dr.average))
    stda = np.std(np.log1p(dr.average))
    if single == True:
        z = (means - np.log1p(X)) / stds
    if average == True:
        z = (meana - np.log1p(X)) / stda
    return z


# Converts the Time to a mm:ss format and mm:ss to seconds
def minsec(x):
    x = str(x)
    if ':' in x:
        t = x.split(':')
        sec = float(t[1])
        min = int(t[0])
        return min * 60 + sec
    else:
        x = float(x)
        sec = x % 60
        min = (x - sec) / 60
        return str(min) + ':' + str(sec)


dr['single_score'] = round(100 / (1 + np.exp(-relayscore(dr.single, single=True))), 2)
dr['average_score'] = round(100 / (1 + np.exp(-relayscore(dr.average, average=True))), 2)

# dr['single'] = minsec(dr.single)
# dr['average'] = minsec(dr.average)
dr.to_csv('WCA_relay.csv', index=False)


def linreg(x, y):
    def z(a, b, x, y):
        s = 0
        for i in range(len(x)):
            s += (x[i] ** a) * (y[i] ** b)
        return s

    c = (z(2, 0, x, y) * z(0, 1, x, y) - z(1, 0, x, y) * z(1, 1, x, y)) / (
            z(0, 0, x, y) * z(2, 0, x, y) - z(1, 0, x, y) ** 2)
    m = (z(0, 0, x, y) * z(1, 1, x, y) - z(1, 0, x, y) * z(0, 1, x, y)) / (
            z(0, 0, x, y) * z(2, 0, x, y) - z(1, 0, x, y) ** 2)
    return m, c

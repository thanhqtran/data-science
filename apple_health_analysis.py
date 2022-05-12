import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xml.etree.ElementTree
import datetime
import xmltodict

# data input
input_path1 = 'path/apple_health_export/export.xml'
with open(input_path1, 'r') as xml_file:
    input_data = xmltodict.parse(xml_file.read())
records = input_data['HealthData']['Record']

# convert xml to dataframe
df = pd.DataFrame(records)
format = '%Y-%m-%d %H:%M:%S %z'
df['@creationDate'] = pd.to_datetime(df['@creationDate'],format=format)
df['@startDate'] = pd.to_datetime(df['@startDate'],format=format)
df['@endDate'] = pd.to_datetime(df['@endDate'],format=format)
df_test = df[df['@type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning']

#to see what kind of data we have
variables = []
for x in df['@type']:
    if x not in variables:
        variables.append(x)
#print(df['@type'].unique())
print(variables)
#to see how datetime variable is formatted
#print(df['@creationDate'])
# output: ['HKQuantityTypeIdentifierHeight', 'HKQuantityTypeIdentifierBodyMass', 'HKQuantityTypeIdentifierStepCount', 'HKQuantityTypeIdentifierDistanceWalkingRunning', 'HKQuantityTypeIdentifierFlightsClimbed', 'HKQuantityTypeIdentifierHeadphoneAudioExposure', 'HKQuantityTypeIdentifierWalkingDoubleSupportPercentage', 'HKQuantityTypeIdentifierWalkingSpeed', 'HKQuantityTypeIdentifierWalkingStepLength', 'HKQuantityTypeIdentifierWalkingAsymmetryPercentage']

#=========extract step counts ==========
x = 2
#call variable
data = df[df['@type'] == variables[x]]
#convert to numeric 
data.loc[:, '@value'] = pd.to_numeric(data.loc[:, '@value'])
#take sum by startdate
data_bystart = data.groupby('@startDate').sum().reset_index()
#set startdate to be datetime index
df_bystart = data_bystart.set_index(['@startDate'])
df_bystart.index = pd.to_datetime(df_bystart.index)
print(df_bystart)

#sum all data of the same day
df_bystart_daysum = df_bystart['@value'].resample('M').sum()
df1 = pd.DataFrame(df_bystart_daysum).reset_index()
df1_copy = df1.rename(columns={'@startDate':'@startDate','@value':variables[x]})
# print(df1_copy.describe())

#sum same month
dist = df[df['@type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning']
dist.loc[:, '@value'] = pd.to_numeric(dist.loc[:, '@value'])
dist_data = dist.groupby('@startDate').sum().reset_index()
dist_data = dist_data.set_index(['@startDate'])
dist_data.index = pd.to_datetime(dist_data.index)
dist_data_bymonth = dist_data['@value'].resample('M').sum()
df3 = pd.DataFrame(dist_data_bymonth)
df3['@avg_walk'] = dist_data['@value'].resample('M').mean()
df3 = df3.reset_index()
df4 = df3.rename(columns={'@startDate':'date','@value':'total_dist','@avg_walk':'avg_dist'})

# draw steps count
fig, ax1 = plt.subplots()
x = df4['date']
y1 = df4['total_dist']
y2 = df4['avg_dist']
plt.xticks(rotation=60)
# barchart = plt.bar(x, y, color='orange', width = 20)
# plt.twinx()
# linechart = plt.plot(x, z, color='blue', marker='o')
# plt.title('Walking distance')
# plt.xlabel('time')
# barchart.ylabel('y')
# linechart.ylabel('z')
# plt.show()

ax2 = ax1.twinx()
ax1.bar(x, y1, color='orange', width = 20)
ax2.plot(x, y2, color='blue', marker='o')

ax1.set_xlabel('Time')
ax1.set_ylabel('Total distance (km)', color='orange')
ax2.set_ylabel('Daily average (km)', color='blue')

plt.title('Walking distance record')
fig.tight_layout()
plt.show()

# color = 'tab:red'
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('average', color=color)
# ax1.plot(z, color=color)
# ax1.tick_params(axis='y', labelcolor=color)

# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# color = 'tab:blue'
# ax2.set_ylabel('total', color=color)  # we already handled the x-label with ax1
# ax2.plot(y, color=color)
# ax2.tick_params(axis='y', labelcolor=color)

# fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()

#============= Extract Sleep counts ==========
#extract sleep counts
sleep_counts = df[df['@type'] == 'HKCategoryTypeIdentifierSleepAnalysis']
sleep_counts['@duration'] = (sleep_counts['@endDate'] - sleep_counts['@startDate']).astype('timedelta64[h]')
sleep_counts_m = sleep_counts.resample('D',on='@creationDate').sum()
plt.plot(sleep_counts_m['@duration'])
plt.show()

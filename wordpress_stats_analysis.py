import matplotlib.dates as mdates
import matplotlib.axes as ax
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

api_key = 'xxxx'
blog_uri = 'nipponkiyoshi.com'
table = ['views', 'postviews', 'referrers',
         'referrers_grouped', 'searchterms', 'clicks', 'videoplays']
days = -1 #unlimited
master_url = 'https://stats.wordpress.com/csv.php?'
x = 1
url = master_url + 'api_key=' + api_key + '&blog_uri=' + \
    blog_uri + '&table=' + table[x] + '&days=' + str(days)
print(url)
#url example: 'https://stats.wordpress.com/csv.php?api_key=xxxx&blog_uri=nipponkiyoshi.com&table=postviews'

#load data
data = pd.read_csv(url)
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.to_csv('path/data.csv')
print(df.stack())


#sort by viewcounts
by_viewcounts = df.groupby(['post_title', 'post_id','post_permalink']).agg(
    {'views': 'sum'})
by_viewcounts_view = by_viewcounts.sort_values(by='views', ascending=False)

#sort by date (days)
by_date = df.groupby('date').agg({'views':'sum'})
by_date_view = by_date.sort_values(by='views',ascending=False)

#sort by month
by_month = df.groupby(pd.Grouper(key='date', freq='M')).agg({'views': 'sum'})
print(by_month)
#plot by month
x = by_month.index
values = by_month['views']
widths = [5 for i in x]
colors = ['darkorange' for i in x]
plt.xlabel('Time')
plt.ylabel('views')
plt.bar(x, values, width=widths, color=colors)
#plt.show()

#sort by year
by_year = df.groupby(pd.Grouper(key='date', freq='Y')).agg({'views': 'sum'})
#print(by_year)
#plot by year
x = by_year.index
values = by_year['views']
widths = [1 for i in x]
colors = ['darkorange' for i in x]
plt.xlabel('Time')
plt.ylabel('views')
plt.plot(values, color='tan', marker='s')
plt.bar(x, values, width = widths, color = colors)
#plt.show()

#extract country view
url_country = 'https://wordpress.com/stats/day/countryviews/nipponkiyoshi.com?startDate=2014-08-28'
start_date = '2014-08-28'
json_api = 'https://developer.wordpress.com/docs/api/console/'

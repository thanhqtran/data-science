import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np

# data
data = pd.DataFrame(pd.read_csv('/path/file.csv', encoding='utf-16'))
data['Date'] = pd.to_datetime(data['Date'])
#extract data that category is NOT in Withdrawal or Gifts
data = data[data['Category'].isin(['Withdrawal', 'Gifts','Other Income','Other Expense']) == False]
data = data[data['Wallet'].isin(['Bank Japan','Cash Japan'])]

#plot money outflows and inflows
plt.figure(figsize=(20,10))
width = 5
plt.bar(data[data['Amount'] < 0]['Date'], data[data['Amount'] < 0]['Amount'], color='tomato', width=width)
plt.bar(data[data['Amount'] > 0]['Date'], data[data['Amount'] > 0]['Amount'], color='cornflowerblue', width=width)
plt.axhline(0, color='grey', lw=0.5)

#treemap (like tableau)
import squarify
import matplotlib
import matplotlib.pyplot as plt

#group by category and plot treemap
data_group = data.groupby('Category')['Amount'].sum()
data_group = data_group.sort_values(ascending=False)
data_group = data_group.reset_index()
expense = data_group[data_group['Amount'] < 0]
income = data_group[data_group['Amount'] > 0]

##===========Expense=============#
#take the top 20 categories by lowest amount of expense
top = 20
expensetop = expense.sort_values(by='Amount', ascending=True)[:top]

# create a color palette, mapped to these values
cmap = matplotlib.cm.viridis
mini=min(expensetop['Amount'])
maxi=max(expensetop['Amount'])
norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
colors = [cmap(norm(value)) for value in expensetop['Amount']]

plt.figure(figsize=(30,15))
plt.rc('font', size=18, family='serif')
squarify.plot(sizes=expensetop['Amount'], label=expensetop['Category'], color=colors, alpha=.7)
plt.axis('off')

##===========Income=============#
# create a color palette, mapped to these values
cmap = matplotlib.cm.viridis_r
mini=min(income['Amount'])
maxi=max(income['Amount'])
norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
colors = [cmap(norm(value)) for value in income['Amount']]

plt.figure(figsize=(30,15))
plt.rc('font', size=16, family='serif')
squarify.plot(sizes=income['Amount'], label=income['Category'], color=colors, alpha=.7)
plt.axis('off')
plt.show()

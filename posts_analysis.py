import pandas as pd 
import pandas_read_xml as pdx
import json 

#Tools -> Export -> Posts
file = 'path/exported_file.xml'

#convert xml to json
data = pdx.read_xml(file, encoding='utf-8')
result = data.to_json()
parsed = json.loads(result)
#normalize results
df = pd.json_normalize(parsed['rss']['0']['channel']['item'])

#clean the data (droping None content)
df.dropna(subset=['content:encoded'], axis=0, inplace=True)

#clean all html tags
import regex as re
from bs4 import BeautifulSoup
import bleach
# clear all html and css tags with bleach 
df['content:encoded'] = df['content:encoded'].apply(lambda x: bleach.clean(x, tags=[], attributes=[], protocols=[], strip_comments=True, strip=True))
#remove '\n', '\t' and '\td' from the text
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'\n|\t|\r', ' ', x))
#remove all 'caption'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'caption', '', x))
#remove all 'figure'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'figure', '', x))
#remove all words containing 'align'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'align', '', x))
#remove all words containing 'center'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'center', '', x))
#remove all words containing 'class'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'class', '', x))
#remove all words containing 'style'
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'style', '', x))
#remove all width 
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'width', '', x))
#remove all aligncenter
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'aligncenter', '', x))
#remove all id
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'id', '', x))
#remove all nbsp
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'nbsp', '', x))
#remove all http
df['content:encoded'] = df['content:encoded'].apply(lambda x: re.sub(r'http\S+', '', x))

#vietnamese word tokenizer
from underthesea import word_tokenize
df['split'] = df['content:encoded'].apply(word_tokenize)
#convert all split to lowercase
df['split'] = df['split'].apply(lambda x: [i.lower() for i in x])
#remove all numbers
df['split'] = df['split'].apply(lambda x: [i for i in x if not i.isdigit()])
#remove all brackets, colons, commas, dots, exclamation marks, question marks, semicolons, slashes, and underscores
df['split'] = df['split'].apply(lambda x: [i for i in x if not i in ['[ =','(','\"','\'', ')', ':', ',', '.', '!', '?', ';', '/','-','[',']', '_', '“', '”', '‘', '’','...','=','+','*','%','$','#','@','^','&','|','~','`','<','>','\\','{','}']])

#remove all commas and dots 
df['split'] = df['split'].apply(lambda x: [i.replace('.', '') for i in x])
#remove all space at the beginning and the end
df['split'] = df['split'].apply(lambda x: [i.strip() for i in x])
#remove beginning with [ =
df['split'] = df['split'].apply(lambda x: [i.replace('[ =', '') for i in x])
#remove all blanks
df['split'] = df['split'].apply(lambda x: [i for i in x if i != ''])

# remove stopwords
import collections 
word_list = []
for i in range(0, df.shape[0]):
    word_list.extend(df.iloc[i]['split'])

stop_words_vn = pd.read_csv('https://raw.githubusercontent.com/thanhqtran/vietnamese-stopwords/master/vietnamese-stopwords.txt', header=None)
stop_words_en = pd.read_csv('https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt', header=None)
stop_words_en_list = stop_words_en[0].tolist()
stop_words_vn_list = stop_words_vn[0].tolist()
stop_words = stop_words_en_list + stop_words_vn_list

# remove stop words
word_list_no_stop = [word for word in word_list if word not in stop_words]
# collector
word_freq = collections.Counter(word_list_no_stop)
# collect top 500 words
word_freq_hist = word_freq.most_common(500)
# make a dataframe
word_freq_df = pd.DataFrame(word_freq_hist, columns=['word', 'freq'])
# sort the dataframe
word_freq_df = word_freq_df.sort_values(by=['freq'], ascending=False)

# make a bar chart (portrait)
top50 = word_freq_df.head(50)
plt.figure(figsize=(7,15))
plt.barh(top50['word'], top50['freq'])
plt.xticks(rotation=90, fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('Frequency', fontsize=15)
plt.ylabel('Word', fontsize=15)
plt.title('nipponkiyoshi.com (top 50 most used words)', fontsize=15)
plt.gca().invert_yaxis()

# make a bar chart (landscape)
import matplotlib.pyplot as plt
top50 = word_freq_df.head(30)
plt.figure(figsize=(12,7))
plt.barh(top50['word'], top50['freq'], color='#ff7f0e', edgecolor='grey')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Frequency', fontsize=15)
plt.ylabel('Word', fontsize=15)
plt.title('nipponkiyoshi.com (top 30 most used words)', fontsize=15)
plt.gca().invert_yaxis()

# make wordcloud
import wordcloud
wc = wordcloud.WordCloud(background_color='white', width=500, height=300, max_words=250, collocations=False, max_font_size=100, random_state=30)
wc=wc.generate(" ".join(word_list_no_stop).lower())
plt.figure(figsize=(15,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")

#make histogram
from matplotlib.ticker import PercentFormatter

plt.figure(figsize=(8,10))
#crate a histogram of frequency distribution of value pair in the dataframe
freq_list = list(word_freq_df['freq'])
plt.hist(freq_list, weights=np.ones(len(freq_list)) / len(freq_list), bins=50, facecolor='blue', edgecolor='black', alpha=0.5)
plt.xlabel('Frequency', fontsize=15)
plt.ylabel('Percent of Words with that frequency', fontsize=15)
plt.title('Frequency Distribution', fontsize=15)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

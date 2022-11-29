import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



#read data
df = pd.read_csv('ViewingActivity.csv')

#drop columns
columns_to_drop = ['Country', 'Bookmark', 'Latest Bookmark', 'Attributes']
df = df.drop(columns = columns_to_drop)
df.reset_index(inplace= True)

#rename columns
df = df.rename(columns = {'Start Time':'Date'})
#Convert Start Time to datetime. Currently it is object
df['Date'] = pd.to_datetime(df['Date'])

#Convert to UTC/EST
df['Date'] = df['Date'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern') 
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['day_of_week'] = df['Date'].dt.dayofweek
df['day_name'] = df['Date'].dt.day_name()

#remove supplemental video from data
df['Supplemental Video Type'].value_counts()
df = df[df['Supplemental Video Type'].isna()]

df[['TV Show', 'Season', 'Episode']] = df['Title'].str.split(':', expand = True, n = 2)

df['Content Type'] = df['Season'].apply(lambda x : 'Movie' if x == None else 'TV Show')
df = df.rename(columns = {'Temp':'Content Type'})

df = df.drop(columns = 'Supplemental Video Type')
df['date_of_month'] = df['Date'].dt.day
df = df[['Profile Name', 'Date', 'date_of_month', 'day_of_week', 'day_name', 'Month', 'Year', 'Duration', 'Title', 'TV Show', 'Season', 'Episode', 'Content Type']]

#print out final spreadsheet
df.to_csv('final_data.csv', index=False)

#############################################
# Data manipulation
pwd = os.getcwd()

# Convert duration HH:MM:SS to number of minutes 
df['Duration (Seconds)'] = df['Duration'].str.split(':').apply(lambda x: int(x[0])*3600 + int(x[1])*60 + int(x[2]))


# Average Watch Time (Seconds) by Day of Week
avg_seconds_per_day = df.groupby('day_name')['Duration (Seconds)'].mean().sort_values()
day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.set_style("darkgrid")
font = {'family': 'serif',
        'color': '#004466',
        'weight': 'normal',
        'size': 16}
plt.figure(figsize=(20,15))
ax = sns.barplot(x = avg_seconds_per_day.index, y = avg_seconds_per_day.values, palette=("Blues_d"), errorbar=None, order=day_of_week)
ax.set_ylabel('Viewing Duration (in Seconds)',fontdict={'size': 13, 'family': 'serif'})
ax.set_xlabel('Day of Week', fontdict={'size': 13, 'family': 'serif'})
ax.set_title('Average Viewing Time per Day (in seconds)', fontdict=font)
ax.tick_params(axis = 'both', labelsize= 12)
plt.savefig(os.path.join(pwd, 'Average Viewing Duration per Day (seconds).png'))



#Top 10 TV Shows by Average Watch time (Seconds)

tv_shows = df[df['Content Type'] == 'TV Show']
most_watched_tv_series = tv_shows.groupby('TV Show')['Duration (Seconds)'].mean().reset_index().sort_values(by = 'Duration (Seconds)', ascending = False) 
font = {'family': 'serif', 'color': '#004466', 'weight': 'normal', 'size': 16} 
plt.figure(figsize=(22, 12)) 
ax = sns.barplot(y = most_watched_tv_series['TV Show'][:10], x = most_watched_tv_series['Duration (Seconds)'][:10], orient = 'h', errorbar=None) 
ax.set_ylabel('TV Series', fontdict={'size': 13, 'family': 'serif'}) 
ax.set_xlabel('Watch Time (in seconds)', fontdict={'size': 13, 'family': 'serif'}) 
ax.set_title('Top 10 TV Shows by Average Duration (seconds)', fontdict=font) 
ax.tick_params(axis = 'both', labelsize= 12) 
plt.savefig(os.path.join(pwd, 'Top 10 TV Shows by Average Duration (seconds).png'))






# Distribution of Watch time Across Months
plt.figure(figsize=(20, 10))
ax = sns.boxplot(x = df['Month'], y = df['Duration (Seconds)'])
ax.set_ylabel('Watch Time (Seconds)', fontdict={'size': 13, 'family': 'serif'})
ax.set_xlabel('Month', fontdict={'size': 13, 'family': 'serif'})
ax.set_title('Distribution of Duration (Seconds) over the months', fontdict=font)
ax.tick_params(axis = 'both', labelsize= 12)
# ax.set_xticklabels(month_name, rotation = 45)
plt.savefig(os.path.join(pwd, 'Distribution of Duration (Seconds) over the months.png'))



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(df.head())
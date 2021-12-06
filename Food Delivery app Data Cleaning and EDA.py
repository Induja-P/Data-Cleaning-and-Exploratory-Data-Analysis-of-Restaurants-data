#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('dark_background')


# In[ ]:


#reading the data
df = pd.read_csv('zomato.csv')
df.head()


# In[ ]:


df.shape


# In[ ]:


df.columns


# In[ ]:


#dropping the columns
df = df.drop(['url', 'address','phone','menu_item','dish_liked','reviews_list'],axis=1)
df.head()


# In[ ]:


df.info()


# In[ ]:


df.drop_duplicates(inplace = True)
df.shape


# In[ ]:


df['rate'].unique()


# In[ ]:


#function to clean the rate column
def fixrate(value):
    if(value=='NEW' or value=='-'):
        return np.nan
    else:
        value = str(value).split('/')
        value = value[0]
        return float(value)

df['rate'] = df['rate'].apply(fixrate)
df['rate'].head()


# In[ ]:


df.rate.isnull().sum()


# In[ ]:


df['rate'].fillna(df['rate'].mean(),inplace=True)
df.rate.isnull().sum()


# In[ ]:


df.info()


# In[ ]:


df.dropna(inplace=True)
df.head()


# In[ ]:


df.info()


# In[ ]:


#renaming columns
df.rename(columns = {'approx_cost(for two people)':'cost2plates','listed_in(type)':'type'},inplace=True)
df.head()


# In[ ]:


df['location'].unique()


# In[ ]:


df['listed_in(city)'].unique()


# In[ ]:


df=df.drop(['listed_in(city)'],axis=1)


# In[ ]:


df.head()


# In[ ]:


df['cost2plates'].unique()


# In[ ]:


#cleaning cost2plates 
def fixcomma(value):
    value = str(value)
    if ',' in value:
        value = value.replace(',','')
        return float(value)
    else:
        return float(value)
    
df['cost2plates'] = df['cost2plates'].apply(fixcomma)
df['cost2plates'].unique()


# In[ ]:


df.head()


# In[ ]:


df['rest_type'].value_counts()


# In[ ]:


rest_types = df['rest_type'].value_counts(ascending = False)
rest_types


# In[ ]:


rest_types_less1000 = rest_types[rest_types<1000]
rest_types_less1000


# In[ ]:


#cleaning rest_types
def fixrest_type(value):
    if(value in rest_types_less1000):
        return 'others'
    else:
        return value
    
df['rest_type'] = df['rest_type'].apply(fixrest_type)
df['rest_type'].value_counts()


# In[ ]:


df['location'].value_counts()


# In[ ]:


locations = df['location'].value_counts(ascending = False)
locations


# In[ ]:


location_less300 = locations[locations<300]
location_less300


# In[ ]:


#cleaning location
def fixlocation(value):
    if(value in location_less300):
        return 'others'
    else:
        return value

df['location'] = df['location'].apply(fixlocation)
df['location'].value_counts()


# In[ ]:


df['cuisines'].value_counts()


# In[ ]:


cuisine = df['cuisines'].value_counts(ascending = False)
cuisine


# In[ ]:


cuisine_less100 = cuisine[cuisine<100]
cuisine_less100


# In[ ]:


#cleaning cuisine
def fixcuisine(value):
    if(value in cuisine_less100):
        return 'others'
    else:
        return value
    
df['cuisines'] = df['cuisines'].apply(fixcuisine)
df['cuisines'].value_counts()


# In[ ]:


df['type'].value_counts()


# In[ ]:


#plotting location,onlinee order,book_tale etc
plt.figure(figsize=(16,10))
ax = sns.countplot(df['location'])
plt.xticks(rotation = 90)


# In[ ]:


plt.figure(figsize=(6,6))
sns.countplot(df['online_order'],palette='inferno')


# In[ ]:


plt.figure(figsize=(6,6))
sns.countplot(df['book_table'],palette='rainbow')


# In[ ]:


plt.figure(figsize=(6,6))
sns.boxplot(x='online_order',y='rate',data = df)


# In[ ]:


plt.figure(figsize=(6,6))
sns.boxplot(x = 'book_table',y = 'rate',data = df)


# In[ ]:


#visualizing location vs order
df_loc = df.groupby(['location','online_order'])['name'].count()
df_loc.to_csv('location_online.csv')
df_loc = pd.read_csv('location_online.csv')
df_loc = pd.pivot_table(df_loc,values=None,index=['location'],columns=['online_order'],fill_value = 0,aggfunc = np.sum)
df_loc


# In[ ]:


df_loc.plot(kind = 'bar',figsize=(15,8))


# In[ ]:


#visualizing location vs book_table
df_book = df.groupby(['location','book_table'])['name'].count()
df_book.to_csv('location_book.csv')
df_book = pd.read_csv('location_book.csv')
df_book = pd.pivot_table(df_book,values=None,index=['location'],columns=['book_table'],fill_value = 0,aggfunc = np.sum)
df_book


# In[ ]:


df_book.plot(kind ='bar',figsize=(15,8))


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='type',y='rate',data = df,palette = 'inferno')


# In[ ]:


#viualizing location vs type
df_type = df.groupby(['location','type'])['name'].count()
df_type.to_csv('location_type.csv')
df_type = pd.read_csv('location_type.csv')
df_type = pd.pivot_table(df_type,values=None,index=['location'],columns=['type'],fill_value = 0,aggfunc = np.sum)
df_type


# In[ ]:


df_type.plot(kind='bar',figsize=(36,8))


# In[ ]:


#visualizing location vs votes
df_vote = df[['location','votes']]
df_vote.drop_duplicates()
df_votes = df_vote.groupby(['location'])['votes'].sum()
df_votes = df_votes.to_frame()
df_votes = df_votes.sort_values('votes',ascending=False)
df_votes.head()


# In[ ]:


plt.figure(figsize=(15,8))
sns.barplot(df_votes.index,df_votes['votes'])
plt.xticks(rotation = 90)


# In[ ]:


#visualizing cuisine vs votes
df_cuisine = df[['cuisines','votes']]
df_cuisine.drop_duplicates()
df_cuisines = df_cuisine.groupby(['cuisines'])['votes'].sum()
df_cuisines = df_cuisines.to_frame()
df_cuisines = df_cuisines.sort_values('votes',ascending=False)
df_cuisines.head()


# In[ ]:


df_cuisin = df_cuisines.iloc[1:,:]
df_cuisin.head()


# In[ ]:


plt.figure(figsize=(15,8))
sns.barplot(df_cuisin.index,df_cuisin['votes'])
plt.xticks(rotation = 90)


# In[ ]:





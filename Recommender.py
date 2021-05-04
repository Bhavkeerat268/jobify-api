#!/usr/bin/env python
# coding: utf-8

# In[2]:

from difflib import get_close_matches

import numpy as np
import pandas as pd

# In[3]:


df = pd.read_csv("final_dataset.csv")
df.drop(df.columns[df.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)

df.isnull().any()

df = df.replace(r'^\s+$', np.nan, regex=True)

# In[7]:


df = df.dropna()

# In[8]:


df.head(5)

# In[9]:


df.columns = df.columns.str.upper()


def combine_features(row):
    return row['CITY'] + " " + row['JOB'] + " " + row['SHIFT'] + " " + row['AGE'] + " " + row['GENDER'] + " " + str(
        row['RANK'])


df["COMBINED_FEATURES"] = df.apply(combine_features, axis=1)

df.head()


class Recommend:
    def recommend(data):
        recommendations = []
        match = get_close_matches(data, df["COMBINED_FEATURES"], n=20, cutoff=0.65)
        final = []
        ranklist = []

        for x in range(len(match)):
            a = match[x].split(' ')
            final.append(a)
            ranklist.append(final[x][5]) # getting ids

        for x in range(len(ranklist)):
            listnew = dict(df.iloc[int(ranklist[x]) - 1])
            recommendations.append(listnew)

        return recommendations


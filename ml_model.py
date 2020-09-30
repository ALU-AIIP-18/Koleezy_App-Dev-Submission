#!/usr/bin/env python
# coding: utf-8

# In[29]:

# This code was written using a python notebook
from sklearn import linear_model # for linear regression modeling
from sklearn import preprocessing # for preprocessing like imputting missing values
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns


# In[30]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[31]:


#Loading data
wind_df=pd.read_csv('wind_generation_data.csv')
solar_df=pd.read_csv('solar_generation_data.csv')


# In[32]:


wind_df.head(3)


# In[33]:


solar_df.head(3)


# In[34]:


#dropping Month and Day Column
solar_df=solar_df.drop(['Month ', 'Day'],1)


# In[35]:


solar_df.head()


# In[36]:


#Exploring the dataframes
wind_df.describe()


# In[37]:


solar_df.describe()


# In[38]:


wind_df.describe()


# In[39]:


#Visualizing the dataframes
pd.DataFrame.hist(wind_df, figsize = [15,15]); 


# Observation: Datapoints for all attributes fall into the same range

# In[40]:


pd.DataFrame.hist(solar_df, figsize = [15,15]);


# Observation: Datapoints for all attributes fall into the same range except Rainfall in mm

# In[41]:


#checking datatypes
wind_df.info()


# In[42]:


solar_df.info()


# Observation: We convert Temp Hi and Temp Low datatype to float

# In[43]:


solar_df


# In[44]:


solar_df['Temp Hi'] = solar_df['Temp Hi'].str.rstrip('°')
solar_df['Temp Low'] = solar_df['Temp Low'].str.rstrip('°')


# In[45]:


solar_df['Temp Hi']=pd.to_numeric(solar_df['Temp Hi'], errors='coerce')
solar_df['Temp Low']=pd.to_numeric(solar_df['Temp Low'], errors='coerce')


# In[46]:


solar_df


# In[47]:


def missing_values_table(df):   #source : https://www.analyticsvidhya.com/blog/2020/06/feature-engineering-guide-data-science-hackathons/
       mis_val = df.isnull().sum()
       mis_val_percent = 100 * df.isnull().sum() / len(df)
       mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
       mis_val_table_ren_columns = mis_val_table.rename(
       columns = {0 : 'Missing Values', 1 : '% of Total Values'})
       mis_val_table_ren_columns = mis_val_table_ren_columns[
           mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
       '% of Total Values', ascending=False).round(1)
       print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"     
           "There are " + str(mis_val_table_ren_columns.shape[0]) +
             " columns that have missing values.")
       return mis_val_table_ren_columns
    
missing_values_table(solar_df) #calling the function


# Replace the missing value in Rainfall column with zero

# In[48]:


solar_df=solar_df.fillna(0)


# In[49]:


missing_values_table(wind_df)


# In[50]:


corr = solar_df.corr()
plt.figure(figsize=(16, 10))
sns.heatmap(corr, xticklabels=corr.columns.values, 
            yticklabels=corr.columns.values,  
            linewidths=.08,                   # set linewidth between entries in matrix
           cbar_kws={"shrink": .7})           # set length of legend on right


# Looking at the weather forecast from the api. there is no values for the 'solar colmn' but we can see from the heatmap that it is highly correlated with CloudCover Percentage. 
# Hence we can drop the column

# In[51]:


solar_df=solar_df.drop('Solar', axis=1)


# Creating prediction model for solar generation plant
# 
# 

# Splitting solar generation data into training and test sets

# In[52]:


X = solar_df.drop(['Power Generated in MW'], axis = 1).values # X are the input (or independent) variables
y = solar_df['Power Generated in MW'].values # y is output (or dependent) variable


# In[53]:


scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)


# In[54]:


# create training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# In[55]:


print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[56]:


#Fitting the model
lm = linear_model.LinearRegression()
solar_model = lm.fit(X_train,y_train)


# In[57]:


#score the model
solar_model.score(X_test, y_test)


# In[58]:


##########################
# SAVE-LOAD using pickle #
##########################
import pickle

# save
with open('solar_model.pkl','wb') as f:
    pickle.dump(solar_model,f)


# In[59]:


wind_df


# In[60]:


# prediction model for wind generation plant



#Splitting solar generation data into training and test sets

X = wind_df.drop(['Power Output'], axis = 1).values # X are the input (or independent) variables
y = wind_df['Power Output'].values # y is output (or dependent) variable

scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# create training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



#Fitting the model
model = RandomForestRegressor(n_jobs=-1)
model.set_params(n_estimators=12)
wind_model = model.fit(X_train,y_train)


#score the model
wind_model.score(X_test, y_test)



# In[61]:


import pickle

# save
with open('wind_model.pkl','wb') as f:
    pickle.dump(wind_model,f)


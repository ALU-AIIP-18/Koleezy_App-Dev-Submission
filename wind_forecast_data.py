
from flask import Flask, request


import pickle
#from sklearn import linear_model
import datetime
import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler


#defining the longitude and latitude needed for the weather api
longitude = 53.556563
latitude = 8.598084

def wind_df():
    #function to create process data from weather api into dataframe
    response = requests.get("http://www.7timer.info/bin/meteo.php?lon=" + str(longitude) + "&lat=" + str(
        latitude) + "4&ac=0&unit=metric&output=json&tzshift=0")   #getting data from api

    #Creating lists
    wind_speed = []
    wind_direction = []
    wind_dict = response.json() #data in dictionary format stored in wind_dict
    imported_date = []
    wind_speed_category = {'1': 0.3, '2': 1.85, '3': 5.7, '4': 9.4, '5': 14,
                           '6': 20.85, '7': 28.55, '8': 34.65, '9': 39.05, '10': 43.8, '11': 48.55, '12': 53.4,
                           '13': 55.9}   #wind speed are categorical variables hence we convert to float
                                          #using grouping info from weather website

    timepoints = len(wind_dict['dataseries'])

    start_date = pd.to_datetime(wind_dict["init"][0:8]) #getting initial date of weather reading

    for j in pd.date_range(start_date, periods=int(float(timepoints) / 8)):
        imported_date.append(j.date())                  #iterating through the dates to obtain 8 days

    #extracting data for 8-day period from the dictionary 'wind_dict'
    for i in range(timepoints):
        wspeed = wind_dict["dataseries"][i]['wind10m']["speed"]
        wdirection = wind_dict["dataseries"][i]['wind10m']["direction"]
        # checking speed category in wind_speed_category_dictionary
        actual_speed = float(wind_speed_category[str(wspeed)])
        wind_speed.append(actual_speed)
        wind_direction.append(float(wdirection))


    wind_speed_avg = []
    wind_direction_avg = []

    i = 0
    j = 8

    #Processing lists to derive average values for wind speed and wind direction
    while i < len(wind_speed):
        w_avg = sum(wind_speed[i:j]) / 8
        wd_avg = sum(wind_direction[i:j]) / 8
        j += 8
        i += 8
        wind_speed_avg.append(w_avg)
        wind_direction_avg.append(wd_avg)

    #storing data in dictionary
    wind_forecast_data = {'wind speed': wind_speed_avg, 'direction': wind_direction_avg}

    wind_df = pd.DataFrame.from_dict(wind_forecast_data) #convert to dataframe

    with open('wind_model.pkl', 'rb') as f:
        model = pickle.load(f)
    X = wind_df
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)    #standardizing the data for prediction
    wind_df['Predicted Power'] = model.predict(X)
    wind_df['Date'] = imported_date      #adding time column to dataframe
    # wind_df.set_index('Date', inplace=True)
    # print(wind_df)
    return wind_df   #returns dataframe







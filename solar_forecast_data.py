
from flask import Flask, request

import requests

import pickle
#from sklearn import linear_model
import datetime
import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler

#defining the longitude and latitude needed for the weather api
longitude = 53.556563
latitude = 8.598084


def solar_df():
    # function to create process data from weather api into dataframe
    response = requests.get("http://www.7timer.info/bin/meteo.php?lon=" + str(longitude) + "&lat=" + str(
        latitude) + "4&ac=0&unit=metric&output=json&tzshift=0")

    # Creating lists
    imported_date = []
    solar_temp = []
    solar_cover = []
    solar_prep = []
    solar_dict = response.json()   #data in dictionary format stored in solar_dict

    solar_prep_category = {'0': 0, '1': 0.25, '2': 1, '3': 4, '4': 10, '5': 16,
                           '6': 30, '7': 50, '8': 75, '9': 75} #precipritation values are categorical variables hence we convert to float
                                          #using grouping info from weather website

    timepoints = len(solar_dict['dataseries'])

    start_date = pd.to_datetime(solar_dict["init"][0:8])  #getting initial date of solar reading

    for j in pd.date_range(start_date, periods=int(float(timepoints) / 8)): #iterating through the dates to obtain 8 days
        imported_date.append(j.date())

    #extracting data for 8-day period from the dictionary 'wind_dict'
    for i in range(timepoints):
        # we extract and convert temperature from  celsius to fahrenheit
        celsius = float(solar_dict["dataseries"][i]['temp2m']) * (9 / 5) + 32
        solar_temp.append(celsius)
        solar_cover.append(float(solar_dict["dataseries"][i]['cloudcover']))
        s_prep = float(solar_dict["dataseries"][i]['prec_amount'])

        actual_solar_prep = float(solar_prep_category[str(int(s_prep))])
        solar_prep.append(actual_solar_prep)

    max_temp = []
    min_temp = []
    new_solar_cover = []
    new_solar_prep = []

    i = 0
    j = 8
    # Processing lists to derive average values for solar_temp(High and Low), max cover and preciitation
    while i < len(solar_cover):
        hightemp = max(solar_temp[i:j])
        lowtemp = min(solar_temp[i:j])
        max_cover = max(solar_cover[i:j])
        max_prep = sum(solar_prep[i:j])
        j += 8
        i += 8
        max_temp.append(hightemp)
        min_temp.append(lowtemp)
        new_solar_cover.append(max_cover)
        new_solar_prep.append(max_prep)
    # storing data in dictionary
    solar_forecast_data = {'Temp Hi': max_temp, 'Temp Low': min_temp, 'Cloud Cover Percentage': new_solar_cover,
                           'Rainfall in mm': new_solar_prep}

    solar_df = pd.DataFrame.from_dict(solar_forecast_data) #convert to dataframe

    with open('solar_model.pkl', 'rb') as f:
        model = pickle.load(f)
    X = solar_df
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)   #standardizing the data for prediction
    solar_df['Predicted Power'] = model.predict(X)
    solar_df['Date'] = imported_date           #adding time column to dataframe

    return solar_df   #returns dataframe



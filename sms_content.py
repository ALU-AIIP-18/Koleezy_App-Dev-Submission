import dashboard
import numpy as np
import pandas as pd
import datetime
def message():
    #This function checks the predicted plant outputs and returns summary statistics
    # in string format to be sent through an SMS
    k=dashboard.get_data()
    my_dict={}  #initializing dictionary
    my_dict['Overall Power'] =str(np.sum(k['Total Expected Power Output']).round(2)) + 'MW'
    my_dict['Avg Solar Power'] = str(np.mean(k['Expected Solar Power'].round(2))) + 'MW'
    my_dict['Max Solar Power'] = str(np.max(k['Expected Solar Power'].round(2))) + 'MW'
    my_dict['Min Solar Power'] = str(np.min(k['Expected Solar Power'].round(2))) + 'MW'
    my_dict['Avg Wind Power'] = str(np.mean(k['Expected Wind Power'].round(2))) + 'MW'
    my_dict['Max Wind Power'] = str(np.max(k['Expected Wind Power'].round(2))) + 'MW'
    my_dict['Min Wind Power'] = str(np.min(k['Expected Wind Power'].round(2))) + 'MW'

    return  my_dict #returns message in dictionary format


def alarm(val):
    #This functioncheckd the predicted datafram for total output less than a particular value
    #and returns an alarm when detected
    k = dashboard.get_data() #import predicted dataframe
    k=k.reset_index()
    my_dict = {}
    value = val
    i = 0
    for rows in k['Total Expected Power Output']:
        if rows < value:
            i += 1
            w = pd.to_datetime(k.loc[k['Total Expected Power Output'] == rows, 'Date'].iloc[0])
            reg_format_date = w.strftime("%d %B %Y")
            my_dict['Alarm' + str(i)] = 'Forecasted combined total of less than ' + str(
                value) + 'MW on ' + reg_format_date + ' !!!'   #creating message
        else:
            {}

    res = not my_dict

    if res == True:
        my_dict={}
        my_dict['Alarm']= 'THERE IS NO ALARM AVAILABLE IN THE PREDICTION CHART' #creating message
    else:
        {}

    return my_dict #returns message in dictionary format

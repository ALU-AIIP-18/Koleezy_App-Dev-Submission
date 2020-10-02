import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import datetime
import pandas as pd
import wind_forecast_data
import solar_forecast_data
import os


def get_dash(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, 
                    server=server,
                    routes_pathname_prefix='/dashapp/',
                    external_stylesheets=external_stylesheets
                    )

    df = get_data() #data to be visualized

    styles = get_styles()

    fig = px.line(df) #lineplot
    fig.update_yaxes(title_text='Power Output in MW')
    fig.update_layout(legend_title_text='Power Type')
    fig.update_traces(mode='markers+lines')

    app.layout = html.Div([
        # html.H6("Change the value in the text box to see callbacks in action!"),
        html.A("SMS forecast summary ", href="/sms_details", style=styles["button_styles"]),
        html.A("Raise Alarm", href="/alarm", style=styles["button_styles"]),
        html.A("Go to Homepage", href="/", style=styles["button_styles"]),
        html.Div("Power Generation Dashboard", id='my-output',
                 style=styles["text_styles"]),
        html.Div(
            dcc.Graph(
                id='example-graph',
                figure=fig
            ),
            style=styles["fig_style"]
        )
    ])

    return app

def readcsv(filename):
    #This function coverts and processes the uploaded maintenance file to a suitable format
    #for merging with predicted solar and wind power outputs
    df=pd.read_csv(filename)
   # df=df.reset_index().to_dict(orient='list')
    data = df
   # mydict={}

    #for keys,values in df.items():
   #     if keys=='index':
   #         pass
   #     else:
    #        mydict[values[0]] = values[1:]


    #data= pd.DataFrame.from_dict(mydict)
    data['Date Of Month'] = data['Date Of Month'].astype(str)
    for rows in data['Date Of Month']:
        if len(rows) < 2:
            data['Date Of Month'][data['Date Of Month'] == rows] = '0' + rows #This coverts date values from
                                                                              #single to double digits

        else:
            pass


    return data   #returns processed data

def get_data():
    #This function combines maintenance and predicted dataframe and process the for visualization in dash
    if os.path.exists('maintenance_file.csv') == False:
        df = pd.DataFrame(columns=['Date Of Month', 'Capacity Available as %'])
        df.to_csv('maintenance_file.csv')
    else:
        {}


    maintenance_df = readcsv("maintenance_file.csv")


    wind_df= wind_forecast_data.wind_df()

    wind_df['Date'] = pd.to_datetime(wind_df['Date'])

    wind_df['Date Of Month'] = wind_df['Date'].dt.strftime('%d')

    wind_df = wind_df.set_index('Date Of Month')

    maintenance_df = maintenance_df.set_index('Date Of Month')

    wind_df = wind_df.merge(maintenance_df, left_index=True, right_index=True, how='left')

    wind_df['Capacity Available as %'] = wind_df['Capacity Available as %'].astype(float)

    wind_df = wind_df.fillna(100)

    wind_df['Available Predicted Power'] = wind_df['Predicted Power'] * (wind_df['Capacity Available as %'] / 100)

    solar_df= solar_forecast_data.solar_df()

    solar_df['Date'] = pd.to_datetime(solar_df['Date'])

    solar_df['Date Of Month'] = solar_df['Date'].dt.strftime('%d')

    solar_df = solar_df.set_index('Date Of Month')

    solar_df = solar_df.merge(maintenance_df, left_index=True, right_index=True, how='left')

    solar_df['Capacity Available as %'] = solar_df['Capacity Available as %'].astype(float)

    solar_df = solar_df.fillna(100)

    solar_df['Available Predicted Power'] = solar_df['Predicted Power'] * (solar_df['Capacity Available as %'] / 100)

    output_df = pd.DataFrame()

    output_df['Date'] = wind_df['Date']
    output_df['Expected Wind Power'] = wind_df['Available Predicted Power']
    output_df['Expected Solar Power'] = solar_df['Available Predicted Power']
    output_df['Total Expected Power Output'] = wind_df['Available Predicted Power'] + solar_df[
        'Available Predicted Power']

    output_df = output_df.set_index('Date')

    output_df = output_df.iloc[1:5]

    return output_df #returns dataframe with Date as index


def get_styles():
    """
    Very good for making the thing beautiful.
    """
    base_styles = {
        "text-align": "center",
        "border": "1px solid #ddd",
        "padding": "7px",
        "border-radius": "2px",
    }
    text_styles = {
        "background-color": "#eee",
        "margin": "auto",
        "width": "50%"
    }
    text_styles.update(base_styles)

    button_styles = {
        "text-decoration": "none",
    }
    button_styles.update(base_styles)

    fig_style = {
        "padding": "10px",
        "width": "80%",
        "margin": "auto",
        "margin-top": "5px"
    }
    fig_style.update(base_styles)
    return {
        "text_styles" : text_styles,
        "base_styles" : base_styles,
        "button_styles" : button_styles,
        "fig_style": fig_style,
    }
   

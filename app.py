#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:34:16 2020

@author: benceszabo
"""

import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim
import dropbox as dx
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import os

token = os.environ["USELESS_WEATHER_PASTCAST_TOKEN"]

dbx = dx.Dropbox(token)

cities_df = pickle.loads(dbx.files_download("/cities.pkl")[1].content)

app = dash.Dash(__name__)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


dat=pd.concat(cities_df,axis=0).reset_index().rename(columns={"level_0": "city"}).drop("level_1",axis=1)

cols=dat.columns.drop(['Years','Months','city'])

dat[cols]=dat[cols].apply(pd.to_numeric,errors="coerce")

fin=dat.groupby("city").agg("mean").reset_index()
fin

geolocator=Nominatim(user_agent="test")

fin["loc"]=fin.city.apply(lambda x: geolocator.geocode(x+",Hungary").raw)

fin

fin['lat']=fin['loc'].apply(lambda x: float(x['lat']))
fin['lon']=fin['loc'].apply(lambda x: float(x['lon']))

fig = px.scatter_mapbox(fin, lat="lat", lon="lon", hover_name="city", hover_data=["Average temperature", "Rain quantity"],
                        color_discrete_sequence=["fuchsia"], zoom=5, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()


# app layout
layout = go.Layout( height = 1000,
                   xaxis_showgrid=False,
                   yaxis_showgrid=False,
                   yaxis_autorange='reversed')


app.layout = html.Div(
    children=[
        html.H1(children=f"Useless weather pastcast"),
        
        dcc.Graph( id='example-graph', 
                  figure = fig)
        
    ]
)

server= app.server

if __name__ == '__main__':
    app.run_server(debug=True)



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

cities = pickle.loads(dbx.files_download("/cities.pkl")[1].content)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dat = pd.concat([cdf.assign(city=k) for k, cdf in cities.items()], axis=0)


cols = dat.columns.drop(["Years", "Months", "city"])

dat[cols] = dat[cols].apply(pd.to_numeric, errors="coerce")

fin = dat.groupby("city").agg("mean").reset_index()

geolocator = Nominatim(user_agent="test")

fin["loc"] = fin.city.apply(lambda x: geolocator.geocode(x + ",Hungary").raw)
fin["lat"] = fin["loc"].apply(lambda x: float(x["lat"]))
fin["lon"] = fin["loc"].apply(lambda x: float(x["lon"]))

fig = px.scatter_mapbox(
    fin,
    lat="lat",
    lon="lon",
    hover_name="city",
    hover_data=["Average temperature", "Rain quantity"],
    color_discrete_sequence=["fuchsia"],
    zoom=5,
    height=300,
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()


# app layout
layout = go.Layout(
    height=1000, xaxis_showgrid=False, yaxis_showgrid=False, yaxis_autorange="reversed"
)

app.layout = html.Div(
    [
        html.H1(children=f"Useless & ugly weather pastcast"),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="map-graph", figure=fig), className="six columns"
                ),
                html.Div(
                        # dcc.Dropdown(
                        #    id="varosok",
                        #    options=[{"label": e, "value": e} for e in cities.keys()],
                        #    value="Budapest",
                        # ),
                        html.Div(children=dcc.Graph(id="diagram"),),
                    className="six columns",
                ),
            ]
        ),
    html.Div(children = "A fent található ábra a KSH 12 időjárás megfigyelő állomásán detektált adatokat mutatja be. "
                        "Részletesebb és jövőbetekintő adatokért keresd az időképet: "),
    ]
)


@app.callback(
    dash.dependencies.Output("diagram", "figure"),
    [  # dash.dependencies.Input("varosok", "value"),
        dash.dependencies.Input("map-graph", "hoverData")
    ],
)
def update_output(hover_value):
    if hover_value is None:
        value = "Budapest"
    else:
        try:
            value = hover_value["points"][0]["hovertext"]
        except (KeyError, IndexError):
            value = "Budapest"
    return px.scatter(
        cities[value],
        x="Years",
        y="Average temperature",
        # color="team",
        hover_data=["Months"],
    )


server = app.server

if __name__ == "__main__":
    app.run_server(port=6972, debug=True)

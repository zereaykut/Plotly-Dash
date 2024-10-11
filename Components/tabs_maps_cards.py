import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

resorts = pd.read_csv("../Data/Ski Resorts/resorts.csv", encoding="ISO-8859-1").assign(
    country_elevation_rank=lambda x: x.groupby("Country", as_index=False)[
        "Highest point"
    ].rank(ascending=False),
    country_price_rank=lambda x: x.groupby("Country", as_index=False)["Price"].rank(
        ascending=False
    ),
    country_slope_rank=lambda x: x.groupby("Country", as_index=False)[
        "Total slopes"
    ].rank(ascending=False),
    country_cannon_rank=lambda x: x.groupby("Country", as_index=False)[
        "Snow cannons"
    ].rank(ascending=False),
)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH, dbc_css])

load_figure_template("MORPH")

app.layout = dbc.Container(
    [
        dcc.Tabs(
            className="dbc",
            children=[
                dbc.Tab(
                    label="Resort Map",
                    children=[
                        html.H1(id="map-title", style={"text-align": "center"}),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dcc.Markdown("**Price Limit**"),
                                                dcc.Slider(
                                                    id="price-slider",
                                                    min=0,
                                                    max=150,
                                                    step=25,
                                                    value=150,
                                                    className="dbc",
                                                ),
                                                html.Br(),
                                                dcc.Markdown("**Feature Preferences**"),
                                                dcc.Checklist(
                                                    id="summer-ski-checklist",
                                                    options=[
                                                        {
                                                            "label": "Has Summer Skiing",
                                                            "value": "Yes",
                                                        }
                                                    ],
                                                    value=[],
                                                ),
                                                dcc.Checklist(
                                                    id="night-ski-checklist",
                                                    options=[
                                                        {
                                                            "label": "Has Night Skiing",
                                                            "value": "Yes",
                                                        }
                                                    ],
                                                    value=[],
                                                ),
                                                dcc.Checklist(
                                                    id="snow-park-checklist",
                                                    options=[
                                                        {
                                                            "label": "Has Snow Park",
                                                            "value": "Yes",
                                                        }
                                                    ],
                                                    value=[],
                                                ),
                                            ]
                                        )
                                    ],
                                    width=3,
                                ),
                                dbc.Col(dcc.Graph(id="resort-map"), width=9),
                            ]
                        ),
                    ],
                ),
                dbc.Tab(
                    label="Country Profiler",
                    children=[
                        html.H1(id="country-title", style={"text-align": "center"}),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Markdown("Select A Continent:"),
                                        dcc.Dropdown(
                                            id="continent-dropdown",
                                            options=resorts["Continent"].unique(),
                                            value="Europe",
                                            className="dbc",
                                        ),
                                        html.Br(),
                                        dcc.Markdown("Select A Country:"),
                                        dcc.Dropdown(
                                            id="country-dropdown",
                                            value="Norway",
                                            className="dbc",
                                        ),
                                        html.Br(),
                                        dcc.Markdown("Select A Metric to Plot:"),
                                        dcc.Dropdown(
                                            id="column-picker",
                                            options=resorts.select_dtypes(
                                                "number"
                                            ).columns[3:],
                                            value="Price",
                                            className="dbc",
                                        ),
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="metric-bar",
                                            hoverData={
                                                "points": [{"customdata": ["Hemsedal"]}]
                                            },
                                        )
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Markdown("### Resort Report Card"),
                                        dbc.Card(
                                            id="resort-name",
                                            style={
                                                "text-align": "center",
                                                "fontSize": 20,
                                            },
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Card(id="elevation-kpi"),
                                                        dbc.Card(id="price-kpi"),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card(id="slope-kpi"),
                                                        dbc.Card(id="cannon-kpi"),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ],
                                    width=3,
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        )
    ],
    style={"width": 1300},
)


@app.callback(
    Output("map-title", "children"),
    Output("resort-map", "figure"),
    Input("price-slider", "value"),
    Input("summer-ski-checklist", "value"),
    Input("night-ski-checklist", "value"),
    Input("snow-park-checklist", "value"),
)
def snow_map(price, summer_ski, night_ski, snow_park):

    title = f"Resorts with a ticket price less than ${price}."

    df = resorts.loc[(resorts["Price"] <= price)]

    if "Yes" in summer_ski:
        df = df.loc[(df["Summer skiing"] == "Yes")]

    if "Yes" in night_ski:
        df = df.loc[(df["Nightskiing"] == "Yes")]

    if "Yes" in snow_park:
        df = df.loc[(df["Snowparks"] == "Yes")]

    fig = px.density_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Total slopes",
        hover_name="Resort",
        center={"lat": 45, "lon": -100},
        zoom=2.5,
        mapbox_style="stamen-terrain",
        color_continuous_scale="blues",
        width=800,
        height=600,
    )
    return title, fig


@app.callback(
    Output("country-dropdown", "options"), Input("continent-dropdown", "value")
)
def country_select(continent):
    return np.sort(resorts.query("Continent == @continent").Country.unique())


@app.callback(
    Output("country-title", "children"),
    Output("metric-bar", "figure"),
    Input("country-dropdown", "value"),
    Input("column-picker", "value"),
)
def plot_bar(country, metric):
    if not country and metric:
        raise PreventUpdate
    title = f"Top Resorts in {country} by {metric}"

    df = resorts.query("Country == @country").sort_values(metric, ascending=False)

    figure = px.bar(df, x="Resort", y=metric, custom_data=["Resort"]).update_xaxes(
        showticklabels=False
    )

    return title, figure


@app.callback(
    Output("resort-name", "children"),
    Output("elevation-kpi", "children"),
    Output("price-kpi", "children"),
    Output("slope-kpi", "children"),
    Output("cannon-kpi", "children"),
    Input("metric-bar", "hoverData"),
)
def report_card(hoverData):
    resort = hoverData["points"][0]["customdata"][0]

    df = resorts.query("Resort == @resort")

    elev_rank = f"Elevation Rank: {int(df["country_elevation_rank"])}"
    price_rank = f"Price Rank: {int(df["country_price_rank"])}"
    slope_rank = f"Slope Rank: {int(df["country_slope_rank"])}"
    cannon_rank = f"Cannon Rank: {int(df["country_cannon_rank"])}"

    return resort, elev_rank, price_rank, slope_rank, cannon_rank


if __name__ == "__main__":
    app.run_server(port=2034)


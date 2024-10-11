import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template

ski_resorts = pd.read_csv("Data/European_Ski_Resorts.csv").drop("Unnamed: 0", axis=1)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

load_figure_template("SLATE")

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col(html.H2(id="title", style={"text-align": "center"})),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Select Options Below:"),
                        html.Hr(),
                        dcc.Slider(
                            id="Elevation Slider",
                            min=0,
                            max=4000,
                            step=500,
                            value=500,
                            marks={i: {"label": f"{i}m"} for i in range(0, 4001, 1000)},
                            className="dbc",
                        ),
                        html.Br(),
                        dcc.Checklist(
                            id="Feature Checklist",
                            options=["Has Snow Park", "Has Night Ski"],
                            value=["Has Snow Park", "Has Night Ski"],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(dbc.Card(dcc.Graph(id="graph")), width=9),
            ]
        ),
    ]
)


@app.callback(
    Output("title", "children"),
    Output("graph", "figure"),
    Input("Elevation Slider", "value"),
    Input("Feature Checklist", "value"),
)
def plot_resort_count(elevation, features):

    ski_resorts_filtered = ski_resorts.query("HighestPoint > @elevation")

    title = f"Ski Resorts with Elevation Over {elevation}M Max Elevation"

    if features == []:
        df = ski_resorts_filtered.groupby("Country", as_index=False).agg(
            ResortCount=("Country", "count")
        )
    elif len(features) == 2:
        df = (
            ski_resorts_filtered.query("Snowparks == 'Yes' and NightSki == 'Yes'")
            .groupby("Country", as_index=False)
            .agg(ResortCount=("Country", "count"))
        )
    elif features == ["Has Snow Park"]:
        df = (
            ski_resorts_filtered.query("Snowparks == 'Yes'")
            .groupby("Country", as_index=False)
            .agg(ResortCount=("Country", "count"))
        )
    else:
        df = (
            ski_resorts_filtered.query("NightSki == 'Yes'")
            .groupby("Country", as_index=False)
            .agg(ResortCount=("Country", "count"))
        )
    fig = (
        px.choropleth(
            df,
            locations="Country",
            color="ResortCount",
            locationmode="country names",
            scope="europe",
        )
        .update_geos(fitbounds="locations")
        .update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar_x=0.85,
            geo_bgcolor="lightblue",
            #         paper_bgcolor="darkblue",
            width=1000,
            height=600,
        )
    )

    return title, fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8335)

